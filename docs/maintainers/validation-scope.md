# Validation Scope

This page documents what `check-rules` and `check-rule-schema` currently validate.

## What Is Checked

- Only packaged markdown rule documents under `src/agentic/resources/rules/` are scanned.
- Each scanned file must be a non-empty markdown document.
- Each rule document must declare YAML frontmatter that matches the current metadata schema.
- The validator checks required section headings and heading order for the document class.
- Navigational documents must expose at least one navigation target, either through `child_paths` or markdown links.
- Metadata references in packaged rule docs are validated semantically against the packaged rules collection, including `child_paths`, `tightens_paths`, and `escalation_paths`.
- The report makes collection coverage visible so every discovered packaged rule document is accounted for.

## What Is Not Checked

- The validator does not compute or verify a merged effective-rule set.
- It does not validate workspace-local profile additions under `agentic/rules/local/`.
- It does not verify general markdown quality beyond the current structural checks.
- It does not prove that every markdown link points to a live file.

## Source Inputs

- [src/agentic/features/workspace/rules/application/queries.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace/rules/application/queries.py)
- [src/agentic/features/workspace/rules/domain/entity.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace/rules/domain/entity.py)
- [src/agentic/features/workspace/rules/domain/service.py](/Users/gorky/Projects/agentic/src/agentic/features/workspace/rules/domain/service.py)

## Boundary

Be exact about current behavior. Do not widen the claim beyond what the current CLI and report builder actually enforce.
