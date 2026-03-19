#!/usr/bin/env python3
import os
import sys
import json
import subprocess

def run_tests():
    # 1. Read config from the dedicated project-specific folder
    config_path = os.path.join(os.getcwd(), 'project-specific', 'arch-config.json')
    if not os.path.exists(config_path):
        print(f"Error: Could not find {config_path}")
        print("Please create 'project-specific/arch-config.json' with your boundaries.")
        sys.exit(1)
        
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
        
    language = config.get('language', 'python')
    rules = config.get('rules', {})
    exclusions = config.get('exclusions', [])
    
    # 2. Run appropriate extractor
    checker_dir = os.path.dirname(os.path.realpath(__file__))
    extractor_map = {
        'python': ['python3', os.path.join(checker_dir, 'extractors', 'python_extractor.py')],
        'typescript': ['node', os.path.join(checker_dir, 'extractors', 'typescript_extractor.js')],
        'php': ['php', os.path.join(checker_dir, 'extractors', 'php_extractor.php')]
    }
    
    if language not in extractor_map:
        print(f"Error: Unsupported language '{language}'")
        sys.exit(1)
        
    cmd = extractor_map[language] + [os.getcwd(), json.dumps(exclusions)]
    
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
