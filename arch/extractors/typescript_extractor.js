#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const targetDir = process.argv[2] || process.cwd();
const exclusions = process.argv[3] ? JSON.parse(process.argv[3]) : [];

function getAllFiles(dirPath, arrayOfFiles) {
    let files;
    try {
        files = fs.readdirSync(dirPath);
    } catch (e) {
        return arrayOfFiles; 
    }
    
    arrayOfFiles = arrayOfFiles || [];
    
    files.forEach(function(file) {
        const fullPath = path.join(dirPath, file);
        const normPath = fullPath.split(path.sep).join('/');
        
        if (exclusions.some(excl => normPath.includes(excl.replace(/\\/g, '/').replace(/^\/|\/$/g, '')))) {
            return;
        }
        
        let stat;
        try {
            stat = fs.statSync(fullPath);
        } catch (e) {
            return;
        }

        if (stat.isDirectory()) {
            arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
        } else {
            if (fullPath.endsWith('.ts') || fullPath.endsWith('.tsx') || fullPath.endsWith('.js') || fullPath.endsWith('.jsx')) {
                arrayOfFiles.push(fullPath);
            }
        }
    });

    return arrayOfFiles;
}

const result = {};

getAllFiles(targetDir).forEach(file => {
    let content;
    try {
        content = fs.readFileSync(file, 'utf8');
    } catch (e) {
        return;
    }
    
    const imports = [];
    const classes = [];
    const functions = [];
    
    function addImport(impPath) {
        if (impPath.startsWith('.')) {
            const fileDir = path.dirname(file);
            const absPath = path.resolve(fileDir, impPath);
            const relToTarget = path.relative(targetDir, absPath).split(path.sep).join('/');
            imports.push(relToTarget);
        } else {
            imports.push(impPath);
        }
    }
    
    const importRegex = /import\s+.*?\s+from\s+['"](.*?)['"]/g;
    let match;
    while ((match = importRegex.exec(content)) !== null) {
        addImport(match[1]);
    }
    
    const dynamicImportRegex = /import\(['"](.*?)['"]\)/g;
    while ((match = dynamicImportRegex.exec(content)) !== null) {
        addImport(match[1]);
    }
    
    const requireRegex = /require\(['"](.*?)['"]\)/g;
    while ((match = requireRegex.exec(content)) !== null) {
        addImport(match[1]);
    }
    
    const classRegex = /class\s+(\w+)/g;
    while ((match = classRegex.exec(content)) !== null) {
        classes.push(match[1]);
    }
    
    const funcRegex = /function\s+(\w+)/g;
    while ((match = funcRegex.exec(content)) !== null) {
        functions.push(match[1]);
    }
    
    const arrowFuncRegex = /(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[\w]+)\s*=>/g;
    while ((match = arrowFuncRegex.exec(content)) !== null) {
        functions.push(match[1]);
    }
    
    const relPath = path.relative(targetDir, file).split(path.sep).join('/');
    result[relPath] = { imports, classes, functions };
});

console.log(JSON.stringify(result));
