# Agentic Issues

## Resolved

- `arch/run_tests.py` only searched for `arch-config.json` in the project root, even though this layout stores it in `agentic/arch-config.json`. The runner now auto-discovers both locations and also supports `--config`.
- `arch/extractors/typescript_extractor.js` used CommonJS `require(...)`, which crashes inside repositories that declare `"type": "module"`. The extractor now uses ESM imports.

## Notes

- The starter `arch-config.json` shipped with placeholder paths that do not match this repository. It has been replaced with repository-specific boundaries so the checker produces meaningful results here.