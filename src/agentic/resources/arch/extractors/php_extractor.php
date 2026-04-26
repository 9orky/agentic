#!/usr/bin/env php
<?php
$targetDir = isset($argv[1]) ? rtrim($argv[1], '/\\') : getcwd();
$exclusions = isset($argv[2]) ? json_decode($argv[2], true) : [];
if (!is_array($exclusions)) $exclusions = [];

function normalize_pattern(string $value): string {
    return trim(str_replace('\\', '/', $value), '/ ');
}

function compile_scope_pattern(string $pattern): string {
    $normalized = normalize_pattern($pattern);
    $regex = '';
    $length = strlen($normalized);

    for ($i = 0; $i < $length; $i++) {
        $current = $normalized[$i];
        if ($current === '*') {
            if ($i + 1 < $length && $normalized[$i + 1] === '*') {
                $regex .= '(.*)';
                $i++;
            } else {
                $regex .= '([^/]*)';
            }
            continue;
        }
        if ($current === '?') {
            $regex .= '([^/])';
            continue;
        }
        $regex .= preg_quote($current, '/');
    }

    return '/^' . $regex . '(?:\/.*)?$/';
}

$compiledExclusions = array_map('compile_scope_pattern', $exclusions);

$result = [];
$filesFound = 0;
$filesExcluded = 0;
$extractionFailures = [];

function relative_path(string $targetDir, string $path): string {
    $relative = str_replace('\\', '/', ltrim(substr($path, strlen($targetDir)), '/\\'));
    return $relative === '' ? '.' : $relative;
}

function lint_php_file(string $path): ?string {
    $command = escapeshellarg(PHP_BINARY) . ' -l ' . escapeshellarg($path) . ' 2>&1';
    $output = [];
    $status = 0;
    exec($command, $output, $status);
    if ($status === 0) {
        return null;
    }

    $message = trim(implode("\n", $output));
    if ($message === '') {
        $message = 'syntax validation failed';
    }
    return $message;
}

function compute_code_line_count(string $content): int {
    $count = 0;
    foreach (preg_split('/\R/', $content) as $line) {
        $stripped = trim($line);
        if (
            $stripped === ''
            || str_starts_with($stripped, '//')
            || str_starts_with($stripped, '#')
            || $stripped === '/*'
            || $stripped === '*/'
            || str_starts_with($stripped, '*')
        ) {
            continue;
        }
        $count++;
    }
    return $count;
}

function line_count_for_content(string $content): int {
    return max(1, substr_count($content, "\n") + 1);
}

function token_line_value($token, int $fallbackLine): int {
    return is_array($token) ? $token[2] : $fallbackLine;
}

function token_text($token): string {
    return is_array($token) ? $token[1] : $token;
}

function is_name_token($token): bool {
    if (!is_array($token)) {
        return false;
    }

    $tokenId = $token[0];
    $valid = [T_STRING];
    if (defined('T_NS_SEPARATOR')) {
        $valid[] = T_NS_SEPARATOR;
    }
    if (defined('T_NAME_QUALIFIED')) {
        $valid[] = T_NAME_QUALIFIED;
    }
    if (defined('T_NAME_FULLY_QUALIFIED')) {
        $valid[] = T_NAME_FULLY_QUALIFIED;
    }
    if (defined('T_NAME_RELATIVE')) {
        $valid[] = T_NAME_RELATIVE;
    }

    return in_array($tokenId, $valid, true);
}

function public_symbol_count(array $classDetails, array $functionDetails): int {
    $publicClasses = 0;
    foreach ($classDetails as $classDetail) {
        if (!empty($classDetail['name']) && $classDetail['name'][0] !== '_') {
            $publicClasses++;
        }
    }

    $publicFunctions = 0;
    foreach ($functionDetails as $functionDetail) {
        if (!empty($functionDetail['name']) && $functionDetail['name'][0] !== '_') {
            $publicFunctions++;
        }
    }

    $publicMethods = 0;
    foreach ($classDetails as $classDetail) {
        foreach ($classDetail['methods'] as $methodDetail) {
            if (!empty($methodDetail['name']) && $methodDetail['name'][0] !== '_') {
                $publicMethods++;
            }
        }
    }

    return $publicClasses + $publicFunctions + $publicMethods;
}

function is_public_method(array $tokens, int $functionIndex): bool {
    for ($index = $functionIndex - 1; $index >= 0; $index--) {
        $token = $tokens[$index];
        if (!is_array($token)) {
            $text = token_text($token);
            if ($text === ';' || $text === '{' || $text === '}') {
                break;
            }
            continue;
        }

        $tokenId = $token[0];
        if (in_array($tokenId, [T_WHITESPACE, T_COMMENT, T_DOC_COMMENT, T_STATIC, T_FINAL, T_ABSTRACT], true)) {
            continue;
        }
        if ($tokenId === T_PRIVATE || $tokenId === T_PROTECTED) {
            return false;
        }
        if ($tokenId === T_PUBLIC) {
            return true;
        }
        break;
    }

    return true;
}

function find_block_end_line(array $tokens, int $startIndex, int $fallbackLine): int {
    $depth = 0;
    $seenBrace = false;
    $currentLine = $fallbackLine;
    $count = count($tokens);

    for ($index = $startIndex; $index < $count; $index++) {
        $token = $tokens[$index];
        $currentLine = token_line_value($token, $currentLine);
        $text = token_text($token);

        if ($text === '{') {
            $depth++;
            $seenBrace = true;
            continue;
        }
        if ($text === '}') {
            if ($seenBrace) {
                $depth--;
                if ($depth === 0) {
                    return $currentLine;
                }
            }
            continue;
        }
        if (!$seenBrace && $text === ';') {
            return $currentLine;
        }
    }

    return $currentLine;
}

if (!is_dir($targetDir)) {
    echo json_encode($result);
    exit(0);
}

$ite = new RecursiveDirectoryIterator($targetDir, RecursiveDirectoryIterator::SKIP_DOTS);
foreach (new RecursiveIteratorIterator($ite) as $file) {
    if (strtolower($file->getExtension()) === 'php') {
        $path = $file->getPathname();
        $relativePath = str_replace('\\', '/', ltrim(substr($path, strlen($targetDir)), '/\\'));
        $filesFound++;

        $skip = false;
        foreach ($compiledExclusions as $pattern) {
            if (preg_match($pattern, $relativePath)) {
                $skip = true;
                break;
            }
        }
        if ($skip) {
            $filesExcluded++;
            continue;
        }

        $content = @file_get_contents($path);
        if ($content === false) {
            $extractionFailures[] = relative_path($targetDir, $path) . ': file_get_contents failed';
            continue;
        }

        $lintError = lint_php_file($path);
        if ($lintError !== null) {
            $extractionFailures[] = relative_path($targetDir, $path) . ': ParseError: ' . $lintError;
            continue;
        }

        $tokens = @token_get_all($content);
        if (!is_array($tokens)) {
            $extractionFailures[] = relative_path($targetDir, $path) . ': token_get_all failed';
            continue;
        }
        $imports = [];
        $classes = [];
        $functions = [];
        $classDetails = [];
        $functionDetails = [];
        $classIndexByName = [];

        $count = count($tokens);
        $currentLine = 1;
        $braceDepth = 0;
        $activeClassName = null;
        $activeClassDepth = 0;

        for ($i = 0; $i < $count; $i++) {
            $token = $tokens[$i];
            $currentLine = token_line_value($token, $currentLine);

            if ($token === '{') {
                $braceDepth++;
                continue;
            }
            if ($token === '}') {
                if ($activeClassName !== null && $braceDepth === $activeClassDepth) {
                    $activeClassName = null;
                    $activeClassDepth = 0;
                }
                $braceDepth = max(0, $braceDepth - 1);
                continue;
            }

            if (!is_array($token)) {
                continue;
            }

            if ($token[0] == T_USE) {
                $usePath = '';
                $j = $i + 1;
                while ($j < $count && token_text($tokens[$j]) !== ';') {
                    if (is_name_token($tokens[$j])) {
                        $usePath .= token_text($tokens[$j]);
                    } elseif ($tokens[$j] === '{' || $tokens[$j] === ',') {
                        break;
                    }
                    $j++;
                }
                if ($usePath !== '') {
                    $imports[] = trim($usePath);
                }
                continue;
            }

            if ($token[0] == T_CLASS) {
                $j = $i + 1;
                while ($j < $count && token_text($tokens[$j]) !== '{') {
                    if (is_array($tokens[$j]) && $tokens[$j][0] == T_STRING) {
                        $className = $tokens[$j][1];
                        $classes[] = $className;
                        $classDetails[] = [
                            'name' => $className,
                            'methods' => [],
                            'line_count' => max(
                                0,
                                find_block_end_line($tokens, $j, $currentLine) - $currentLine + 1
                            ),
                        ];
                        $classIndexByName[$className] = count($classDetails) - 1;
                        $activeClassName = $className;
                        $activeClassDepth = $braceDepth + 1;
                        break;
                    }
                    $j++;
                }
                continue;
            }

            if ($token[0] == T_FUNCTION) {
                $j = $i + 1;
                while ($j < $count && token_text($tokens[$j]) !== '(') {
                    if (is_array($tokens[$j]) && $tokens[$j][0] == T_STRING) {
                        $functionName = $tokens[$j][1];
                        $lineCount = max(
                            0,
                            find_block_end_line($tokens, $j, $currentLine) - $currentLine + 1
                        );
                        if ($activeClassName !== null && array_key_exists($activeClassName, $classIndexByName)) {
                            if ($functionName !== '__construct' && is_public_method($tokens, $i)) {
                                $classDetails[$classIndexByName[$activeClassName]]['methods'][] = [
                                    'name' => $functionName,
                                    'line_count' => $lineCount,
                                ];
                            }
                        } else {
                            $functions[] = $functionName;
                            $functionDetails[] = [
                                'name' => $functionName,
                                'line_count' => $lineCount,
                                'cyclomatic_complexity' => null,
                            ];
                        }
                        break;
                    }
                    $j++;
                }
            }
        }

        $metrics = [
            'line_count' => line_count_for_content($content),
            'code_line_count' => compute_code_line_count($content),
            'public_symbol_count' => public_symbol_count($classDetails, $functionDetails),
            'max_method_count_per_class' => array_reduce(
                $classDetails,
                fn (int $carry, array $item): int => max($carry, count($item['methods'])),
                0,
            ),
        ];

        $result[$relativePath] = [
            'imports' => $imports,
            'classes' => $classes,
            'functions' => $functions,
            'class_details' => $classDetails,
            'function_details' => $functionDetails,
            'metrics' => $metrics,
        ];
    }
}

if (!empty($extractionFailures)) {
    fwrite(STDERR, "Extractor failed to analyze PHP files:\n" . implode("\n", $extractionFailures) . "\n");
    exit(1);
}

echo json_encode([
    'files' => $result,
    'summary' => [
        'files_found' => $filesFound,
        'files_excluded' => $filesExcluded,
        'files_checked' => count($result),
    ],
]);
