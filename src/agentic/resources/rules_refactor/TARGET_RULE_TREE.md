# Target Rule Tree

## Intent

Replace the legacy rules tree with a smaller, schema-first system that is easier to scan, easier to edit, and easier to validate.

## Design Goals

1. Separate routing, policy, and execution concerns.
2. Prefer fields and checklists over prose.
3. Keep each document responsible for one decision level only.
4. Make execution documents the most structured artifacts.
5. Preserve markdown readability while moving schema into frontmatter.
6. Make folder traversal explicit and progressive.
7. Keep schema vocabulary and document vocabulary identical.
8. Let project-specific rules tighten shared rules without replacing them.

## Target Tree

```text
rules/
  INDEX.md
  structure/
    INDEX.md
    MODULE.md
    feature/
      INDEX.md
      FEATURE.md
      layers/
        INDEX.md
        LAYERS.md
        FILE_TREE.md
  project/
    INDEX.md
    structure/
      INDEX.md
      MODULE.md
      feature/
        INDEX.md
        FEATURE.md
        layers/
          INDEX.md
          LAYERS.md
          FILE_TREE.md
  architecture/
    INDEX.md
    OWNERSHIP.md
    BOUNDARIES.md
    DEPENDENCIES.md
  execution/
    INDEX.md
    BIG_PICTURE.md
    STEP.md
  change/
    INDEX.md
    REFACTORING.md
  verification/
    INDEX.md
    TESTING.md
```

## Navigation Contract

1. Every rules folder uses `INDEX.md` as its only entrypoint.
2. When entering a folder, read `INDEX.md` first and do not descend until it points to a child.
3. Navigational indexes decide whether to stop, descend, or cross-link to another branch.
4. Policy and execution documents stay as leaf files by default.
5. Create a subfolder only when a leaf becomes complex enough to need its own router and subordinate files.
6. Direct reads of a child leaf are allowed only when the user points to it explicitly or a parent index routes there.
7. Each index should let the agent stop early when the current task does not require deeper traversal.
8. Project-specific indexes are entered only after the matching shared branch is already in scope.

## Frontmatter Contract

Every document should declare enough metadata to make traversal enforceable:

1. `doc_class`
2. `rule_kind`
3. `audience`
4. `purpose`
5. `applies_when`
6. `tags`
7. `read_directly`
8. `scope`
9. `tightens_paths` for project-specific documents
10. `entrypoint` for navigational indexes
11. `read_strategy` for navigational indexes
12. `child_paths` for navigational indexes
13. `escalation_paths` for policy and execution documents

## Tree Rationale

1. `INDEX.md` at the root is the only global router.
2. `structure/` is the primary branch for classifying a target folder before deeper rules are applied.
3. `project/` tightens shared rules with repository-local structure and naming constraints.
4. `architecture/` answers placement, ownership, seam, and dependency questions after structure is known.
5. `execution/` defines the executable documents used before and during implementation.
6. `change/` governs reshaping existing code and deciding when fresh-slice work is required.
7. `verification/` governs test strategy and completion proof.
8. Leaf rules remain files unless complexity justifies a deeper routed subtree.

## Document Classes

### Navigational

Use for navigation only.

Required shape:

1. stored as `INDEX.md`
2. frontmatter with purpose, applies-when, entrypoint, read strategy, and child paths
3. one link section
4. optional short notes

Forbidden shape:

1. long policy prose
2. duplicated guidance already owned by a child rule

Role:

1. a navigational document is the router role in the tree

### Policy

Use for stable architectural or verification rules.

Required shape:

1. frontmatter with purpose and applies-when
2. compact field or checklist sections
3. review checks
4. optional escalation links only when more detail is needed

Stored as:

1. a leaf markdown file under a routed folder
2. a subfolder only when the rule needs a local router and subordinate leaves

Preferred content:

1. rules as yes-or-no checks
2. short field lists for required decisions
3. minimal prose for exceptions only

### Execution

Use for executable design artifacts.

Required shape:

1. frontmatter with stage metadata
2. exactly one tree section
3. contract fields
4. review checks
5. handoff checks when the next execution stage depends on approval
6. optional escalation links only when architecture or verification guidance is needed

Stored as:

1. a leaf markdown file under `execution/`
2. a subfolder only when a specific execution artifact needs its own routed subtree

Stage rules:

1. `execution/BIG_PICTURE.md` uses a file tree first and forbids signatures.
2. `execution/STEP.md` uses an implementation tree first and requires signatures.
3. step files are the same artifact family as big picture at finer detail.

## Document Inventory

### INDEX.md

Class: navigational

Purpose:

1. choose the governing branch for the current task

Children:

1. `architecture/INDEX.md`
2. `structure/INDEX.md`
3. `project/INDEX.md`
4. `execution/INDEX.md`
5. `change/INDEX.md`
6. `verification/INDEX.md`

### structure/INDEX.md

Class: navigational

Purpose:

1. classify the target folder at the shallowest structural level that fits

Children:

1. `MODULE.md`
2. `feature/INDEX.md`

### structure/MODULE.md

Class: policy

Purpose:

1. define the base rule for any module-shaped folder of program files

Core checks:

1. the folder owns one coherent responsibility
2. the public API is minimal
3. internal files are not exported without need
4. deeper specialization is applied only when the structure really requires it

### structure/feature/INDEX.md

Class: navigational

Purpose:

1. route stricter module rules when the target is a feature-shaped module

Children:

1. `FEATURE.md`
2. `layers/INDEX.md`

### structure/feature/FEATURE.md

Class: policy

Purpose:

1. define stricter ownership and boundary expectations for a feature module

Core checks:

1. the module owns a user-visible or business capability
2. the feature boundary is explicit
3. cross-feature access stays narrow
4. the feature still exposes only a minimal API

### structure/feature/layers/INDEX.md

Class: navigational

Purpose:

1. route layered-module rules when layering is part of the contract

Children:

1. `LAYERS.md`
2. `FILE_TREE.md`

### structure/feature/layers/LAYERS.md

Class: policy

Purpose:

1. define allowed layers and dependency direction inside a layered module

Core checks:

1. each responsibility is placed in one layer
2. dependency direction is explicit
3. cross-layer shortcuts are rejected
4. layers exist because they constrain the design, not as decoration

### structure/feature/layers/FILE_TREE.md

Class: policy

Purpose:

1. define the deterministic file-tree growth rules for layered modules

Core checks:

1. the tree follows the chosen layer model
2. new files are added in the owning layer first
3. public seams are stable and minimal
4. tree growth reflects responsibility, not convenience

### project/INDEX.md

Class: navigational

Purpose:

1. route repository-local rule supplements after the shared branch is already known

Children:

1. `structure/INDEX.md`

### project/structure/INDEX.md

Class: navigational

Purpose:

1. route repository-local structural supplements for this workspace

Children:

1. `MODULE.md`
2. `feature/INDEX.md`

### project/structure/MODULE.md

Class: policy

Purpose:

1. tighten the shared module rule with repository-local package and seam conventions

Core checks:

1. module roots expose a minimal package seam
2. importable package roots keep `__init__.py` minimal
3. bootstrap or CLI entrypoints stay explicit
4. local conventions do not widen the shared module API rule

### project/structure/feature/INDEX.md

Class: navigational

Purpose:

1. route repository-local feature supplements after shared feature classification

Children:

1. `FEATURE.md`
2. `layers/INDEX.md`

### project/structure/feature/FEATURE.md

Class: policy

Purpose:

1. tighten feature structure for this repository's feature packages

Core checks:

1. feature roots stay small
2. feature roots expose only explicit seams
3. nested modules carry most internal feature logic
4. feature-local rules do not bypass shared feature boundaries

### project/structure/feature/layers/INDEX.md

Class: navigational

Purpose:

1. route repository-local layer naming and tree constraints

Children:

1. `LAYERS.md`
2. `FILE_TREE.md`

### project/structure/feature/layers/LAYERS.md

Class: policy

Purpose:

1. define the allowed layer names and dependency meaning used in this repository

Core checks:

1. layer names come from the project convention
2. missing layers are allowed when the module does not need them
3. dependency meaning for each named layer is explicit
4. new layer names require a project-rule change first

### project/structure/feature/layers/FILE_TREE.md

Class: policy

Purpose:

1. define repository-local file-tree expectations for layered feature modules

Core checks:

1. canonical package roots are explicit
2. canonical layer folders use project-approved names only
3. feature-root seams stay small
4. new tree branches require a structural reason, not convenience

### architecture/INDEX.md

Class: navigational

Purpose:

1. route ownership, boundary, and dependency questions

Children:

1. `OWNERSHIP.md`
2. `BOUNDARIES.md`
3. `DEPENDENCIES.md`

### architecture/OWNERSHIP.md

Class: policy

Purpose:

1. decide which feature, module, or layer owns a responsibility

Core checks:

1. owning enclosure named
2. owning module named
3. owning layer named
4. no split ownership without an explicit seam

### architecture/BOUNDARIES.md

Class: policy

Purpose:

1. decide public boundary, seam, and internal privacy rules

Core checks:

1. public seam named
2. private internals protected
3. no deep imports
4. no widened API without a real consumer need

### architecture/DEPENDENCIES.md

Class: policy

Purpose:

1. decide allowed dependency direction

Core checks:

1. direction explicit
2. no circular dependency
3. parent depends on child seam only
4. child never depends on consumer

### execution/INDEX.md

Class: navigational

Purpose:

1. route between big-picture and step execution artifacts

Children:

1. `BIG_PICTURE.md`
2. `STEP.md`

### execution/BIG_PICTURE.md

Class: execution

Purpose:

1. define phase-level execution before step files exist

Required sections:

1. file tree
2. goal
3. phase list
4. acceptance
5. open questions

Optional sections:

1. execution frame
2. strategic model

Core checks:

1. file tree is first
2. files and folders only
3. no signatures
4. phases translate directly to step files

### execution/STEP.md

Class: execution

Purpose:

1. define one approved phase at implementation detail

Required sections:

1. implementation tree
2. goal
3. step contract
4. execution
5. verification
6. completion

Core checks:

1. implementation tree is first
2. signatures are included
3. scope is narrow and verifiable
4. completion state is explicit

### change/INDEX.md

Class: navigational

Purpose:

1. route code-change work that reshapes existing implementation

Children:

1. `REFACTORING.md`

### change/REFACTORING.md

Class: policy

Purpose:

1. govern target-design refactoring and fresh-slice decisions

Core checks:

1. target design chosen first
2. fresh-slice decision explicit
3. legacy structure not treated as authority
4. verified swap required before cleanup

### verification/INDEX.md

Class: navigational

Purpose:

1. route proof and testing questions

Children:

1. `TESTING.md`

### verification/TESTING.md

Class: policy

Purpose:

1. govern seam selection, test scope, and assertion quality

Core checks:

1. public seam named
2. smallest proving scope chosen
3. no test-only production seams
4. assertions prove behavior, not internals

## Legacy Assumptions To Remove

1. A rule document needs large prose sections to be useful.
2. Every concern needs its own router and subrouter chain.
3. Planning is a separate artifact family from execution.
4. Repeated guidance belongs in body prose instead of schema checks.
5. Feature guidance should be the default starting point before module classification.
6. Every leaf rule needs its own folder and `INDEX.md`.
7. Shared rules alone should imply repository-local layer names or file-tree choices.

## Migration Sequence

1. Build the new tree under `rules_refactor/` first.
2. Author the router documents before policy and execution leaves.
3. Author the `structure/` branch early because module classification is the base abstraction.
4. Pilot the `execution/` branch because it has the clearest schema and the highest current verbosity.
5. Add `project/` after shared structure so repository-local constraints tighten the shared defaults.
6. Author `architecture/` after structure because placement depends on structural classification.
7. Migrate `change/` and `verification/` after the pilot proves the shape works.
8. Compare the new tree against representative tasks before replacing the packaged legacy tree.

## Approval Gates

1. The tree is smaller than the legacy tree at the top level.
2. Every document has one clear responsibility.
3. Router documents route only.
4. Policy documents read mostly as checklists and fields.
5. Execution documents are stronger forms, not essays.
6. The new tree can be authored from `schemas.py` without special-case document logic.