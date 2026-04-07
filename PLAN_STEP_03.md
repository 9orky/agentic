# Implementation Tree

- agentic/
- agentic/rules/
- agentic/rules/local/
- agentic/rules/local/execution/
- agentic/rules/local/execution/BIG_PICTURE.md
- agentic/rules/local/execution/STEP.md
- agentic/rules/local/structure/
- agentic/rules/local/structure/FEATURE_LAYERS.md
- agentic/rules/local/structure/FEATURE_FILE_TREE.md
- agentic/rules/local/structure/FEATURE.md
- agentic/rules/local/structure/MODULE.md

# Goal

Reduce the local rule branch to a small project-specific profile that an agent can generate and a user can fine-tune without duplicating shared policy.

# Step Contract

- Inputs: [PLAN.md](PLAN.md), the shared semantic baseline from [PLAN_STEP_01.md](PLAN_STEP_01.md), and the aligned docs from [PLAN_STEP_02.md](PLAN_STEP_02.md).
- Outputs: trimmed local execution and structure rules that keep only repo-specific naming, seam, scaffold, and similar profile decisions in the proposed structured format.
- Scope: local execution and structure rules only.
- Out-of-scope: shared rule edits, maintainership docs, runtime docs, and routing index updates.
- Owning layer: `application`
- Dependency direction: depends only on approved earlier outputs from Steps 01 and 02.
- Earlier-layer dependencies: Step 01 shared rule baseline and Step 02 documentation contract.
- Root seam updates: none.

# Execution

1. Remove universal workflow naming from local execution rules once it exists in shared execution guidance.
2. Keep only repo-specific execution tightening that remains necessary after the shared baseline is in place.
3. Reduce local structure rules to the selected layer names, Python seam conventions, starter files, and other narrow repo profile decisions.
4. Reshape local content so it matches the proposed structured local override format and separates observed facts from narrowing decisions.

# Verification

- Confirm local rules no longer restate shared workflow or generic layered-architecture policy.
- Confirm every remaining local decision is clearly repo-specific and reviewable.
- Confirm local artifacts are small enough to be agent-generated consistently and user-reviewed directly.

# Completion

- The local branch is a thin specialization layer instead of a second general rule system.
- Phase 04 can update routing based on a stable reduced local surface.
