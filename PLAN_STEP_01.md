# Implementation Tree

- src/
- src/agentic/
- src/agentic/resources/
- src/agentic/resources/rules/
- src/agentic/resources/rules/shared/
- src/agentic/resources/rules/shared/execution/
- src/agentic/resources/rules/shared/execution/BIG_PICTURE.md
- src/agentic/resources/rules/shared/execution/STEP.md
- src/agentic/resources/rules/shared/structure/
- src/agentic/resources/rules/shared/structure/FEATURE_LAYERS.md
- src/agentic/resources/rules/shared/structure/FEATURE_FILE_TREE.md

# Goal

Define the shared-rule baseline for universal planning artifact naming and generic layered or onion structure so later local artifacts only carry discovered project-specific narrowing.

# Step Contract

- Inputs: [PLAN.md](PLAN.md), current shared execution rules, current shared structure rules, and the current local tightenings that will be reduced later.
- Outputs: revised shared execution and shared structure rules that define universal workflow naming and reusable layered dependency guidance.
- Scope: shared rule semantics only; no local rule reduction in this step.
- Out-of-scope: maintainership docs, runtime docs, local rule rewrites, and agent routing updates.
- Owning layer: `domain`
- Dependency direction: none; this is the first approved step and establishes the semantic baseline.
- Earlier-layer dependencies: none.
- Root seam updates: none.

# Execution

1. Promote plan artifact naming from local execution guidance into shared execution guidance.
2. Expand shared structure guidance so layered or onion architecture is available as a reusable option without hardcoding this repo's exact layer names.
3. Define explicit limits on what local overrides may narrow after repository discovery.
4. Keep shared guidance generic enough that it can govern other repositories without importing this repo's Python starter-file conventions.

# Verification

- Confirm the shared execution rules are the single source for universal `PLAN.md` and `PLAN_STEP_0X.md` naming.
- Confirm shared structure rules describe inward dependency constraints generically rather than with repo-specific names.
- Confirm the remaining local override surface is clearly smaller than before and limited to discovered repo profile choices.

# Completion

- Shared execution and structure rule semantics are ready for downstream documentation alignment.
- Phase 02 can consume the approved shared baseline without redefining workflow or layering semantics.
