#!/usr/bin/env python3
import os
import sys
import json
import subprocess

import argparse


def resolve_config_path(project_root, checker_dir, explicit_config_path=None):
    candidates = []

    if explicit_config_path:
        candidates.append(os.path.abspath(explicit_config_path))

    candidates.extend([
        os.path.join(project_root, 'arch-config.json'),
        os.path.join(project_root, 'agentic', 'arch-config.json'),
        os.path.join(os.path.dirname(checker_dir), 'arch-config.json'),
    ])

    seen = set()
    for candidate in candidates:
        normalized = os.path.normpath(candidate)
        if normalized in seen:
            continue
        seen.add(normalized)

        if os.path.exists(normalized):
            return normalized

    return None

def run_tests():
    parser = argparse.ArgumentParser(description="Architecture Rule Checker")
    parser.add_argument("--project-root", type=str, default=os.getcwd(), help="Path to the project root directory")
    parser.add_argument("--config", type=str, help="Path to arch-config.json")
    args = parser.parse_args()
    
    project_root = os.path.abspath(args.project_root)
    checker_dir = os.path.dirname(os.path.realpath(__file__))

    # 1. Read config from the project root
    config_path = resolve_config_path(project_root, checker_dir, args.config)
    if not config_path:
        print("Error: Could not find arch-config.json")
        print("Looked in the project root, project_root/agentic, and next to this script.")
        print("Please copy arch-config.json.dist to arch-config.json and configure your boundaries.")
        sys.exit(1)
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    language = config.get('language', 'python')
    rules = config.get('rules', {})
    exclusions = config.get('exclusions', [])
    
    # 2. Run appropriate extractor
    extractor_map = {
        'python': ['python3', os.path.join(checker_dir, 'extractors', 'python_extractor.py')],
        'typescript': ['node', os.path.join(checker_dir, 'extractors', 'typescript_extractor.js')],
        'php': ['php', os.path.join(checker_dir, 'extractors', 'php_extractor.php')]
    }
    
    if language not in extractor_map:
        print(f"Error: Unsupported language '{language}'")
        sys.exit(1)
        
    cmd = extractor_map[language] + [project_root, json.dumps(exclusions)]
    
    try:
        # Run extractor and read JSON map from stdout
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        architecture_map = json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Extractor script failed: {e.stderr}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Failed to parse extractor output as JSON: {e}\nRaw Output: {result.stdout}")
        sys.exit(1)
        
    # 3. Evaluate rules
    violations = []
    boundaries = rules.get('boundaries', [])
    
    for filepath, data in architecture_map.items():
        # norm paths for cross-platform matches
        norm_path = filepath.replace('\\', '/')
        
        for rule in boundaries:
            source_prefix = rule.get('source', '')
            disallowed = rule.get('disallow', [])
            
            if norm_path.startswith(source_prefix):
                for imp in data.get('imports', []):
                    for dis in disallowed:
                        if dis in imp:
                            violations.append(f"[VIOLATION] {filepath}\n  -> Layer '{source_prefix}' cannot depend on '{dis}'\n  -> Offending import: '{imp}'")

    # 4. Report Results to Agent
    if violations:
        print("\n=== Architectural Violations Detected ===")
        print("\n".join(violations))
        sys.exit(1)
    else:
        print("Architecture Check Passed! No violations found.")
        sys.exit(0)

if __name__ == '__main__':
    run_tests()
