#!/usr/bin/env python3
import ast
import os
import sys
import json

def extract(directory, exclusions):
    result = {}
    for root, dirs, files in os.walk(directory):
        # Apply exclusions to directories
        dirs_to_remove = []
        for d in dirs:
            dir_path = os.path.join(root, d).replace('\\', '/')
            if any(excl.replace('\\', '/').strip('/') in dir_path for excl in exclusions):
                dirs_to_remove.append(d)
        for d in dirs_to_remove:
            dirs.remove(d)
            
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                norm_path = path.replace('\\', '/')
                
                if any(excl.replace('\\', '/').strip('/') in norm_path for excl in exclusions):
                    continue
                    
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                        tree = ast.parse(content, filename=path)
                        imports = []
                        classes = []
                        functions = []
                        
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    imports.append(alias.name)
                            elif isinstance(node, ast.ImportFrom):
                                if node.level > 0:
                                    rel_dir = os.path.dirname(os.path.relpath(path, directory)).replace('\\', '/')
                                    parts = rel_dir.split('/') if rel_dir and rel_dir != '.' else []
                                    if node.level > 1:
                                        parts = parts[:-(node.level - 1)]
                                    base = ".".join(parts) if parts else ""
                                    
                                    if node.module:
                                        resolved = f"{base}.{node.module}" if base else node.module
                                        imports.append(resolved)
                                    else:
                                        for alias in node.names:
                                            resolved = f"{base}.{alias.name}" if base else alias.name
                                            imports.append(resolved)
                                elif node.module:
                                    imports.append(node.module)
                            elif isinstance(node, ast.ClassDef):
                                classes.append(node.name)
                            elif isinstance(node, ast.FunctionDef):
                                functions.append(node.name)
                                
                        relPath = os.path.relpath(path, directory).replace('\\', '/')
                        result[relPath] = {
                            "imports": imports,
                            "classes": classes,
                            "functions": functions
                        }
                except SyntaxError:
                    pass
                except UnicodeDecodeError:
                    pass
                        
    return result

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    exclusions = json.loads(sys.argv[2]) if len(sys.argv) > 2 else []
    print(json.dumps(extract(target_dir, exclusions)))
