#!/usr/bin/env php
<?php
$targetDir = isset($argv[1]) ? rtrim($argv[1], '/\\') : getcwd();
$exclusions = isset($argv[2]) ? json_decode($argv[2], true) : [];
if (!is_array($exclusions)) $exclusions = [];

$result = [];

if (!is_dir($targetDir)) {
    echo json_encode($result);
    exit(0);
}

$ite = new RecursiveDirectoryIterator($targetDir, RecursiveDirectoryIterator::SKIP_DOTS);
foreach (new RecursiveIteratorIterator($ite) as $file) {
    if (strtolower($file->getExtension()) === 'php') {
        $path = $file->getPathname();
        
        $skip = false;
        foreach ($exclusions as $ex) {
            $normalizedExcl = str_replace(['\\', '/'], DIRECTORY_SEPARATOR, trim($ex, '/\\ '));
            if (strpos($path, $normalizedExcl) !== false) {
                $skip = true;
                break;
            }
        }
        if ($skip) continue;

        $content = @file_get_contents($path);
        if ($content === false) continue;
        
        $tokens = @token_get_all($content);
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
        
        $relPath = ltrim(substr($path, strlen($targetDir)), '/\\');
        $result[str_replace('\\', '/', $relPath)] = [
            'imports' => $imports,
            'classes' => $classes,
            'functions' => $functions
        ];
    }
}

echo json_encode($result);
