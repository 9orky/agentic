#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const targetDir = process.argv[2] || process.cwd();
const exclusions = process.argv[3] ? JSON.parse(process.argv[3]) : [];

function normalizePattern(value) {
    return value.replace(/\\/g, '/').replace(/^\/+|\/+$/g, '').trim();
}

function escapeRegexChar(char) {
    return char.replace(/[|\\{}()[\]^$+?.]/g, '\\$&');
}

function compileScopePattern(pattern) {
    const normalized = normalizePattern(pattern);
    let regex = '^';
    for (let index = 0; index < normalized.length; index += 1) {
        const current = normalized[index];
        if (current === '*') {
            if (normalized[index + 1] === '*') {
                regex += '(.*)';
                index += 1;
            } else {
                regex += '([^/]*)';
            }
            continue;
        }
        if (current === '?') {
            regex += '([^/])';
            continue;
        }
        regex += escapeRegexChar(current);
    }
    regex += '(?:/.*)?$';
    return new RegExp(regex);
}

const exclusionPatterns = exclusions.map(compileScopePattern);
let filesFound = 0;
let filesExcluded = 0;

function isSourceFile(fullPath) {
    return fullPath.endsWith('.ts') || fullPath.endsWith('.tsx') || fullPath.endsWith('.js') || fullPath.endsWith('.jsx');
}

function isExcluded(fullPath) {
    const relativePath = path.relative(targetDir, fullPath).split(path.sep).join('/');
    return exclusionPatterns.some(pattern => pattern.test(relativePath));
}

function countSourceFiles(dirPath) {
    let files;
    try {
        files = fs.readdirSync(dirPath);
    } catch (e) {
        return 0;
    }

    let total = 0;
    files.forEach(function(file) {
        const fullPath = path.join(dirPath, file);

        let stat;
        try {
            stat = fs.statSync(fullPath);
        } catch (e) {
            return;
        }

        if (stat.isDirectory()) {
            total += countSourceFiles(fullPath);
            return;
        }

        if (isSourceFile(fullPath)) {
            total += 1;
        }
    });

    return total;
}

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

        let stat;
        try {
            stat = fs.statSync(fullPath);
        } catch (e) {
            return;
        }

        if (isExcluded(fullPath)) {
            if (stat.isDirectory()) {
                const excludedCount = countSourceFiles(fullPath);
                filesFound += excludedCount;
                filesExcluded += excludedCount;
                return;
            }

            if (isSourceFile(fullPath)) {
                filesFound += 1;
                filesExcluded += 1;
            }
            return;
        }

        if (stat.isDirectory()) {
            arrayOfFiles = getAllFiles(fullPath, arrayOfFiles);
        } else {
            if (isSourceFile(fullPath)) {
                filesFound += 1;
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

console.log(JSON.stringify({
    files: result,
    summary: {
        files_found: filesFound,
        files_excluded: filesExcluded,
        files_checked: Object.keys(result).length,
    },
}));