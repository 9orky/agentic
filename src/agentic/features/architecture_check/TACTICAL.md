# Architecture Agreement Validation Tactical Plan

## Purpose

This document defines the tactical model for the `Architecture Agreement Validation` bounded context.

It explains how the `architecture_check` feature, which is the current implementation root for that bounded context, represents dependency structure, rules, analyzers, and enforcement responsibilities.

## Scope

This tactical plan governs `src/agentic/features/architecture_check/`.

It covers the current `checker` module and the bounded-context seams exposed through the feature root.

It should stay aligned with the repo-level strategic model in [DDD.md](../../../DDD.md).

## Model Decisions

1. The `architecture_check` feature root is the current implementation root for the `Architecture Agreement Validation` bounded context, so this tactical artifact uses the strategic bounded-context name rather than the feature nickname as its source of truth.
2. Dependency structure is modeled around a graph-centered domain with nodes, edges, and policy analyzers.
3. Configuration loading and extractor execution stay in infrastructure because they adapt external inputs and runtimes rather than express domain invariants.
4. Application commands, queries, and report-building services orchestrate config loading, extraction, graph construction, evaluation, and presentation-ready reporting without owning the rule language itself.
5. UI owns the registered `check` command, summary presentation, and text and JSON rendering while depending only on application seams.
6. No domain-owned repository contract exists today because the bounded context evaluates transient extracted state rather than loading a long-lived aggregate from persistence.

## Concept Catalog

| Concept | Classification | Identity | Invariants | Lifecycle | Owning Module | Owning Layer |
| --- | --- | --- | --- | --- | --- | --- |
| Dependency graph | Entity and aggregate root | Identified by the set of tracked node identifiers and edges for one evaluation run | Nodes and edges must remain internally consistent as edges are added | Built per extraction or evaluation run and discarded after reporting | `checker` | `domain` |
| Node | Entity member | Identified by node id inside the graph | Node identity is stable within one graph and carries a declared kind | Created when the graph discovers or adds a node | `checker` | `domain` |
| Edge | Entity member | Identified by from-node, to-node, and edge kind inside the graph | An edge must preserve its directed relationship and kind | Created when the graph records a dependency relationship | `checker` | `domain` |
| Architecture check config | Value object | Identified by the parsed configuration content for one run | Configuration must satisfy the bounded context's config-validation rules | Loaded from config input, then consumed by application and domain logic | `checker` | `domain` |
| Rule set | Value object | Identified by the parsed boundary, tag, and flow rule payload for one run | Boundary, tag, and flow subsets must remain internally consistent as one config-owned rule set | Created during config parsing and reused during evaluation | `checker` | `domain` |
| Boundary rule | Value object | Identified by one source pattern and its allow and disallow rules | Matching semantics must remain deterministic and consistent | Created during config parsing and reused during evaluation | `checker` | `domain` |
| Config tag rule | Value object | Identified by tag name and config match pattern | Config-declared tag matching must remain deterministic under the bounded context's parsing rules | Created during config parsing and reused during rule-set translation | `checker` | `domain` |
| Flow rule set | Value object | Identified by the configured layer and analyzer settings | Flow analyzers must use the declared layer ordering and module-tag semantics consistently | Created during config parsing and consumed during evaluation | `checker` | `domain` |
| Flow analyzer config | Value object | Identified by one enabled analyzer and its active layer-order context | Analyzer settings must preserve the same layer and module-tag semantics used by flow evaluation | Derived during policy evaluation and discarded after one evaluation flow | `checker` | `domain` |
| Tag rule | Value object | Identified by tag name and match pattern | Tag matching must remain deterministic under the bounded context's pattern semantics | Created during config parsing and reused during evaluation | `checker` | `domain` |
| Node selector | Value object | Identified by one path-pattern and optional tag-selection strategy | Selector matching must remain deterministic and preserve the bounded context's path and tag semantics | Created during rule translation and reused during evaluation | `checker` | `domain` |
| Pattern match | Value object | Identified by one successful selector match and its capture set | Captured groups must preserve selector match ordering and remain tied to one selector result | Created during selector matching and discarded after evaluation logic consumes it | `checker` | `domain` |
| Dependency rule | Value object | Identified by one translated source selector, target selector, and allow-disallow meaning | Dependency matching must preserve the same translated semantics derived from the configured boundary rules | Derived during policy translation and reused during one evaluation flow | `checker` | `domain` |
| Extracted file | Value object | Identified by one extracted file path in an extraction run | Extracted file data must preserve the extractor contract expected by graph building | Created when runtime output is parsed and reused while building a graph | `checker` | `domain` |
| Extraction summary | Value object | Identified by one extractor summary payload for a run | File counts must remain internally consistent for files found, excluded, and checked | Created when runtime output is parsed and then attached to one extraction result | `checker` | `domain` |
| Extraction result | Value object | Identified by one extractor output for a run | Extracted files and summary must satisfy the bounded context's extractor-contract validation rules | Created when runtime output is parsed and then consumed by graph building and reporting | `checker` | `domain` |
| Architecture policy evaluator | Domain service and policy | One evaluator for direct architectural policy checks | Boundary and flow rules must be evaluated against the same extracted graph and config semantics | Constructed per evaluation flow and discarded after use | `checker` | `domain` |
| Backward-flow, no-cycles, and no-reentry analyzers | Domain service and policy | One analyzer per flow concern | Each analyzer must preserve the bounded context's definition of illegal flow | Constructed when a run enables the analyzer and then discarded | `checker` | `domain` |
| Edge rule violation | Value object | Identified by one violating source-target relationship plus the blocking rule pattern pair | Violation details must preserve the offending edge and the translated rule semantics that blocked it | Created during evaluation and then grouped, rendered, or serialized for reporting | `checker` | `domain` |
| Flow violation | Value object | Identified by one violating path, analyzer type, and violation index | Violation details must preserve the exact failing path and analyzer meaning | Created during evaluation and then grouped, rendered, or serialized for reporting | `checker` | `domain` |
| Architecture summary | Application DTO | Identified by one describe-config result | Summary output groups the configuration view exposed to callers | Created for query output and then rendered or returned | `checker` | `application` |
| Check result | Application DTO | Identified by one architecture-check run | Result output must group extracted summary, findings, and outcome coherently | Created for command output and then rendered or returned | `checker` | `application` |
| Architecture report builder | Application coordinator | One orchestration service for config loading, extraction, graph building, evaluation, and report assembly | Each build must apply one runtime, one resolved extractor spec, one graph build, and one evaluation flow coherently | Constructed by application seams, invoked per report build, then discarded | `checker` | `application` |
| Config loader | Infrastructure adapter | One adapter for reading architecture-agreement files | Only supported config locations and formats should be read into the bounded context | Instantiated when configuration must be loaded from disk | `checker` | `infrastructure` |
| Extractor runtime | Infrastructure adapter | One adapter for running language-specific extraction tooling | Runtime interaction must respect the extractor contract expected by the bounded context | Instantiated when dependency extraction must run | `checker` | `infrastructure` |
| Extractor spec registry | Infrastructure adapter | One adapter for resolving supported extractor implementations | Supported language extractors and contracts must be resolved deterministically | Instantiated when the application flow chooses an extractor | `checker` | `infrastructure` |
| Violation dot renderer | Infrastructure adapter | One adapter for graph-report rendering | Rendered output must reflect the evaluated violation structure accurately | Instantiated when dot output is requested | `checker` | `infrastructure` |
| Architecture check CLI | UI contract | One registered delivery surface for the `check` command | Delivery depends only on application seams and preserves command options, output-format behavior, and exit-code semantics | Registered at CLI startup and invoked per command call | `checker` | `ui` |
| Check summary presenter and text/JSON violation views | UI contract | Identified by one rendered summary or violation view for an architecture-check run | Rendering must remain delivery-only and format application outputs without owning rule evaluation behavior | Instantiated per UI flow and discarded after rendering | `checker` | `ui` |

## Aggregate And Repository Decisions

1. `Dependency graph` is the current aggregate root for one evaluation run.
2. `Node` and `Edge` are treated as graph-owned entity members rather than free-floating aggregate roots.
3. No domain-owned repository contract exists today because evaluation runs operate on transient extracted state rather than a persisted aggregate lifecycle.
4. If future work requires cached graph snapshots or persisted policy histories, revisit repository ownership explicitly instead of routing persistence concerns straight into infrastructure by habit.

## Open Questions

1. Should `Node` and `Edge` remain under the entity anchor, or should they eventually be reframed as graph-owned members with a narrower public surface?
2. Should the bounded context expose a clearer aggregate boundary in code around `DependencyGraph` if more graph behavior moves into the domain?
3. Is there any future need for a domain-facing repository if extracted graph state becomes durable across runs?