# Implementation Tree

- docs/
- docs/maintainers/
- docs/maintainers/rule-system.md
- docs/runtime/
- docs/runtime/workspace-contract.md

# Goal

Align maintainership and runtime documentation with the new split: shared rules own universal workflow and optional layered structure, while local rules hold narrow agent-generated project profile decisions.

# Step Contract

- Inputs: [PLAN.md](PLAN.md) and the approved shared-rule baseline from [PLAN_STEP_01.md](PLAN_STEP_01.md).
- Outputs: updated maintainership and runtime docs that describe the discovery-to-generation-to-review workflow and the structured local override format.
- Scope: documentation alignment only.
- Out-of-scope: rewriting local rule files, changing agent routing indexes, or changing validation code.
- Owning layer: `infrastructure`
- Dependency direction: depends only on the approved semantic baseline from Step 01.
- Earlier-layer dependencies: Step 01 shared execution and structure rule decisions.
- Root seam updates: none.

# Execution

1. Update maintainership docs to describe the shared versus local split honestly and explicitly.
2. Update runtime docs to explain that local outputs are agent-generated, structured, and later user-tuned.
3. Document the proposed local override format, including required frontmatter fields and fixed body sections.
4. Avoid implying that runtime code computes an effective merged rule graph if that behavior still does not exist.

# Verification

- Confirm docs consistently describe the init -> discover -> generate -> review workflow.
- Confirm docs distinguish discovered facts from narrowing decisions in the proposed local format.
- Confirm docs do not claim merge behavior that the runtime does not implement.

# Completion

- Human-facing docs are aligned with the new model before local rule rewrites begin.
- Phase 03 can reduce local rules against a stable documented contract.
