#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';

const targetDir = process.argv[2] || process.cwd();
const exclusions = process.argv[3] ? JSON.parse(process.argv[3]) : [];

function buildLineStarts(content) {
    const lineStarts = [0];
    for (let index = 0; index < content.length; index += 1) {
        if (content[index] === '\n') {
            lineStarts.push(index + 1);
        }
    }
    return lineStarts;
}

function lineNumberAt(lineStarts, index) {
    let low = 0;
    let high = lineStarts.length - 1;
    while (low <= high) {
        const middle = Math.floor((low + high) / 2);
        if (lineStarts[middle] <= index) {
            low = middle + 1;
        } else {
            high = middle - 1;
        }
    }
    return high + 1;
}

function lineSpan(lineStarts, startIndex, endIndex) {
    return Math.max(lineNumberAt(lineStarts, endIndex) - lineNumberAt(lineStarts, startIndex) + 1, 0);
}

function computeCodeLineCount(content) {
    let total = 0;
    content.split('\n').forEach(line => {
        const stripped = line.trim();
        if (!stripped || stripped.startsWith('//') || stripped === '/*' || stripped === '*/' || stripped.startsWith('*')) {
            return;
        }
        total += 1;
    });
    return total;
}

function publicSymbolCount(
    classDetails,
    functionDetails,
    exportedClassNames,
    exportedFunctionNames,
    publicMethodCountsByClass,
    extraPublicSurfaceCount,
) {
    const publicClasses = classDetails.filter(
        item => exportedClassNames.has(item.name) && item.name && !item.name.startsWith('_'),
    ).length;
    const publicFunctions = functionDetails.filter(
        item => exportedFunctionNames.has(item.name) && item.name && !item.name.startsWith('_'),
    ).length;
    const publicMethods = classDetails.reduce(
        (total, item) => total + (exportedClassNames.has(item.name) ? (publicMethodCountsByClass.get(item.name) || 0) : 0),
        0,
    );
    return publicClasses + publicFunctions + publicMethods + extraPublicSurfaceCount;
}

function collectExportSurface(content, localClassNames, localFunctionNames) {
    const exportedClassNames = new Set();
    const exportedFunctionNames = new Set();
    let extraPublicSurfaceCount = 0;

    const localClassNameSet = new Set(localClassNames);
    const localFunctionNameSet = new Set(localFunctionNames);

    const namedExportRegex = /\bexport\s*\{([^}]+)\}(?:\s*from\s*['"][^'"]+['"])?/g;
    let match;
    while ((match = namedExportRegex.exec(content)) !== null) {
        const exportBody = match[1];
        const isReExport = /\bfrom\s*['"][^'"]+['"]/.test(match[0]);
        const specifiers = exportBody
            .split(',')
            .map(item => item.trim())
            .filter(Boolean);

        for (const specifier of specifiers) {
            const [localRaw, exportedRaw] = specifier.split(/\s+as\s+/i).map(item => item.trim());
            const localName = localRaw;
            const exportedName = exportedRaw || localRaw;

            if (isReExport) {
                extraPublicSurfaceCount += 1;
                continue;
            }

            if (exportedName === 'default') {
                if (localClassNameSet.has(localName)) {
                    exportedClassNames.add(localName);
                } else if (localFunctionNameSet.has(localName)) {
                    exportedFunctionNames.add(localName);
                } else {
                    extraPublicSurfaceCount += 1;
                }
                continue;
            }

            if (localClassNameSet.has(localName)) {
                exportedClassNames.add(localName);
                continue;
            }
            if (localFunctionNameSet.has(localName)) {
                exportedFunctionNames.add(localName);
                continue;
            }
            extraPublicSurfaceCount += 1;
        }
    }

    const exportAllMatches = content.match(/\bexport\s+\*\s+from\s+['"][^'"]+['"]/g) || [];
    extraPublicSurfaceCount += exportAllMatches.length;

    const defaultValueExportRegex = /\bexport\s+default\s+(?!class\b)(?!function\b)(?!async\s+function\b)([A-Za-z_$][\w$]*)\s*;?/g;
    while ((match = defaultValueExportRegex.exec(content)) !== null) {
        const exportedName = match[1];
        if (localClassNameSet.has(exportedName)) {
            exportedClassNames.add(exportedName);
        } else if (localFunctionNameSet.has(exportedName)) {
            exportedFunctionNames.add(exportedName);
        } else {
            extraPublicSurfaceCount += 1;
        }
    }

    const anonymousDefaultClassMatches = content.match(/\bexport\s+default\s+class\b(?!\s+[A-Za-z_$][\w$]*)/g) || [];
    const anonymousDefaultFunctionMatches = content.match(/\bexport\s+default\s+(?:async\s+)?function\b(?!\s+[A-Za-z_$][\w$]*)/g) || [];
    extraPublicSurfaceCount += anonymousDefaultClassMatches.length + anonymousDefaultFunctionMatches.length;

    return { exportedClassNames, exportedFunctionNames, extraPublicSurfaceCount };
}

function findMatchingBrace(content, openBraceIndex) {
    let depth = 0;
    let inSingleQuote = false;
    let inDoubleQuote = false;
    let inTemplate = false;
    let inLineComment = false;
    let inBlockComment = false;

    for (let index = openBraceIndex; index < content.length; index += 1) {
        const current = content[index];
        const next = content[index + 1];

        if (inLineComment) {
            if (current === '\n') {
                inLineComment = false;
            }
            continue;
        }
        if (inBlockComment) {
            if (current === '*' && next === '/') {
                inBlockComment = false;
                index += 1;
            }
            continue;
        }
        if (inSingleQuote) {
            if (current === '\\') {
                index += 1;
                continue;
            }
            if (current === '\'') {
                inSingleQuote = false;
            }
            continue;
        }
        if (inDoubleQuote) {
            if (current === '\\') {
                index += 1;
                continue;
            }
            if (current === '"') {
                inDoubleQuote = false;
            }
            continue;
        }
        if (inTemplate) {
            if (current === '\\') {
                index += 1;
                continue;
            }
            if (current === '`') {
                inTemplate = false;
            }
            continue;
        }

        if (current === '/' && next === '/') {
            inLineComment = true;
            index += 1;
            continue;
        }
        if (current === '/' && next === '*') {
            inBlockComment = true;
            index += 1;
            continue;
        }
        if (current === '\'') {
            inSingleQuote = true;
            continue;
        }
        if (current === '"') {
            inDoubleQuote = true;
            continue;
        }
        if (current === '`') {
            inTemplate = true;
            continue;
        }
        if (current === '{') {
            depth += 1;
            continue;
        }
        if (current === '}') {
            depth -= 1;
            if (depth === 0) {
                return index;
            }
        }
    }
    return -1;
}

function isWithinRanges(index, ranges) {
    return ranges.some(range => index >= range.start && index <= range.end);
}

function collectClassDetails(content, lineStarts) {
    const classDetails = [];
    const classRanges = [];
    const exportedClassNames = new Set();
    const publicMethodCountsByClass = new Map();
    const classRegex = /\b(?:export\s+(?:default\s+)?)?class\s+([A-Za-z_$][\w$]*)[^{]*\{/g;
    let match;
    while ((match = classRegex.exec(content)) !== null) {
        const className = match[1];
        const declarationText = match[0];
        const openBraceIndex = content.indexOf('{', match.index);
        if (openBraceIndex < 0) {
            continue;
        }
        const closeBraceIndex = findMatchingBrace(content, openBraceIndex);
        if (closeBraceIndex < 0) {
            continue;
        }

        const body = content.slice(openBraceIndex + 1, closeBraceIndex);
        const methods = [];
        const seenMethods = new Set();
        let publicMethodCount = 0;
        const methodRegex = /(?:^|\n)\s*((?:public|protected|private|static|async|get|set|readonly)\s+)*([#A-Za-z_$][\w$]*)\s*\([^()\n]*\)\s*\{/g;
        let methodMatch;
        while ((methodMatch = methodRegex.exec(body)) !== null) {
            const modifiers = (methodMatch[1] || '').trim();
            const methodName = methodMatch[2];
            if (seenMethods.has(methodName)) {
                continue;
            }
            seenMethods.add(methodName);
            const methodStart = openBraceIndex + 1 + methodMatch.index;
            const methodOpenBrace = body.indexOf('{', methodMatch.index);
            const methodBraceIndex = openBraceIndex + 1 + methodOpenBrace;
            const methodCloseBraceIndex = findMatchingBrace(content, methodBraceIndex);
            methods.push({
                name: methodName,
                line_count: methodCloseBraceIndex >= 0
                    ? lineSpan(lineStarts, methodStart, methodCloseBraceIndex)
                    : null,
            });
            if (
                !methodName.startsWith('#')
                && !methodName.startsWith('_')
                && !modifiers.includes('private')
                && !modifiers.includes('protected')
                && methodName !== 'constructor'
            ) {
                publicMethodCount += 1;
            }
        }

        classDetails.push({
            name: className,
            methods,
            line_count: lineSpan(lineStarts, match.index, closeBraceIndex),
        });
        classRanges.push({ start: match.index, end: closeBraceIndex });
        if (/\bexport\b/.test(declarationText)) {
            exportedClassNames.add(className);
        }
        publicMethodCountsByClass.set(className, publicMethodCount);
    }

    return { classDetails, classRanges, exportedClassNames, publicMethodCountsByClass };
}

function collectFunctionDetails(content, lineStarts, classRanges) {
    const functionDetails = [];
    const functionNames = [];
    const seenNames = new Set();
    const exportedFunctionNames = new Set();

    function addFunction(name, startIndex, endIndex, isExported) {
        if (!name || seenNames.has(name) || isWithinRanges(startIndex, classRanges)) {
            return;
        }
        seenNames.add(name);
        functionNames.push(name);
        if (isExported) {
            exportedFunctionNames.add(name);
        }
        functionDetails.push({
            name,
            line_count: endIndex >= startIndex ? lineSpan(lineStarts, startIndex, endIndex) : null,
            cyclomatic_complexity: null,
        });
    }

    const functionRegex = /\b(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\([^)]*\)\s*\{/g;
    let match;
    while ((match = functionRegex.exec(content)) !== null) {
        const openBraceIndex = content.indexOf('{', match.index);
        const closeBraceIndex = openBraceIndex >= 0 ? findMatchingBrace(content, openBraceIndex) : -1;
        addFunction(
            match[1],
            match.index,
            closeBraceIndex >= 0 ? closeBraceIndex : match.index,
            /\bexport\b/.test(match[0]),
        );
    }

    const arrowFunctionRegex = /\b(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?(?:\([^)]*\)|[A-Za-z_$][\w$]*)\s*=>\s*(\{)?/g;
    while ((match = arrowFunctionRegex.exec(content)) !== null) {
        const hasBlockBody = match[2] === '{';
        const openBraceIndex = hasBlockBody ? content.indexOf('{', match.index) : -1;
        const closeBraceIndex = hasBlockBody && openBraceIndex >= 0 ? findMatchingBrace(content, openBraceIndex) : match.index;
        addFunction(
            match[1],
            match.index,
            closeBraceIndex >= 0 ? closeBraceIndex : match.index,
            /\bexport\b/.test(match[0]),
        );
    }

    return { functionDetails, functionNames, exportedFunctionNames };
}

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
const extractionFailures = [];

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
        extractionFailures.push(`${path.relative(targetDir, dirPath).split(path.sep).join('/') || '.'}: ${e.name}: ${e.message}`);
        return 0;
    }

    let total = 0;
    files.forEach(function(file) {
        const fullPath = path.join(dirPath, file);

        let stat;
        try {
            stat = fs.statSync(fullPath);
        } catch (e) {
            extractionFailures.push(`${path.relative(targetDir, fullPath).split(path.sep).join('/')}: ${e.name}: ${e.message}`);
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
        extractionFailures.push(`${path.relative(targetDir, dirPath).split(path.sep).join('/') || '.'}: ${e.name}: ${e.message}`);
        return arrayOfFiles;
    }

    arrayOfFiles = arrayOfFiles || [];

    files.forEach(function(file) {
        const fullPath = path.join(dirPath, file);

        let stat;
        try {
            stat = fs.statSync(fullPath);
        } catch (e) {
            extractionFailures.push(`${path.relative(targetDir, fullPath).split(path.sep).join('/')}: ${e.name}: ${e.message}`);
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
        extractionFailures.push(`${path.relative(targetDir, file).split(path.sep).join('/')}: ${e.name}: ${e.message}`);
        return;
    }

    const imports = [];
    const lineStarts = buildLineStarts(content);

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

    const {
        classDetails,
        classRanges,
        exportedClassNames: directlyExportedClassNames,
        publicMethodCountsByClass,
    } = collectClassDetails(content, lineStarts);
    const { functionDetails, functionNames, exportedFunctionNames: directlyExportedFunctionNames } = collectFunctionDetails(content, lineStarts, classRanges);
    const classes = classDetails.map(item => item.name);
    const functions = functionNames;
    const {
        exportedClassNames,
        exportedFunctionNames,
        extraPublicSurfaceCount,
    } = collectExportSurface(content, classes, functions);
    for (const className of directlyExportedClassNames) {
        exportedClassNames.add(className);
    }
    for (const functionName of directlyExportedFunctionNames) {
        exportedFunctionNames.add(functionName);
    }
    const metrics = {
        line_count: content.split('\n').length,
        code_line_count: computeCodeLineCount(content),
        public_symbol_count: publicSymbolCount(
            classDetails,
            functionDetails,
            exportedClassNames,
            exportedFunctionNames,
            publicMethodCountsByClass,
            extraPublicSurfaceCount,
        ),
        max_method_count_per_class: classDetails.reduce(
            (maximum, item) => Math.max(maximum, item.methods.length),
            0,
        ),
    };

    const relPath = path.relative(targetDir, file).split(path.sep).join('/');
    result[relPath] = {
        imports,
        classes,
        functions,
        class_details: classDetails,
        function_details: functionDetails,
        metrics,
    };
});

if (extractionFailures.length > 0) {
    console.error(`Extractor failed to analyze TypeScript files:\n${extractionFailures.join('\n')}`);
    process.exit(1);
}

console.log(JSON.stringify({
    files: result,
    summary: {
        files_found: filesFound,
        files_excluded: filesExcluded,
        files_checked: Object.keys(result).length,
    },
}));
