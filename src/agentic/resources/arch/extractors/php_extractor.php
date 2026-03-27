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

        $count = count($tokens);
        for ($i = 0; $i < $count; $i++) {
            if (is_array($tokens[$i])) {
                if ($tokens[$i][0] == T_USE) {
                    $usePath = '';
                    $j = $i + 1;
                    while ($j < $count && $tokens[$j] !== ';') {
                        if (is_array($tokens[$j]) && ($tokens[$j][0] == T_STRING || $tokens[$j][0] == T_NS_SEPARATOR)) {
                            $usePath .= $tokens[$j][1];
                        } else if ($tokens[$j] === '{' || $tokens[$j] === ',') {
                            break;
                        }
                        $j++;
                    }
                    if (!empty($usePath)) {
                        $imports[] = trim($usePath);
                    }
                } elseif ($tokens[$i][0] == T_CLASS) {
                    $j = $i + 1;
                    while ($j < $count && $tokens[$j] !== '{') {
                        if (is_array($tokens[$j]) && ($tokens[$j][0] == T_STRING)) {
                            $classes[] = $tokens[$j][1];
                            break;
                        }
                        $j++;
                    }
                } elseif ($tokens[$i][0] == T_FUNCTION) {
                    $j = $i + 1;
                    while ($j < $count && $tokens[$j] !== '(') {
                        if (is_array($tokens[$j]) && ($tokens[$j][0] == T_STRING)) {
                            $functions[] = $tokens[$j][1];
                            break;
                        }
                        $j++;
                    }
                }
            }
        }

        $result[$relativePath] = [
            'imports' => $imports,
            'classes' => $classes,
            'functions' => $functions
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