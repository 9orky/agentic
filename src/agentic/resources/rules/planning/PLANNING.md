# Planning Rules

Document Class: navigational

## Purpose

Use this file to route planning work.

## Use This When

1. Use this file when the task is planning work.
2. Choose the child document that matches the current planning stage.

## Available Options

| Document | Information You Can Obtain |
| --- | --- |
| [phases/BIG_PICTURE.md](phases/BIG_PICTURE.md) | the high-level planning contract for scope, capabilities, placement, phases, risks, and acceptance criteria |
| [../ddd/DDD.md](../ddd/DDD.md) | the strategic and tactical domain-modeling rules, plus the contract for a project-local `DDD.md` artifact when planning changes business language or boundaries |
| [phases/STEPS.md](phases/STEPS.md) | the step-planning contract for sequencing, step sections, implementation trees, and completion criteria |

## Navigation Rule

1. Start with [phases/BIG_PICTURE.md](phases/BIG_PICTURE.md).
2. The first planning output is the big-picture plan only.
3. If the plan changes business language, bounded contexts, context relationships, or material domain structure, follow [../ddd/DDD.md](../ddd/DDD.md) before locking the plan.
4. Move to [phases/STEPS.md](phases/STEPS.md) only after the high-level plan is accepted.
5. After approval, split the accepted plan into executable step files named `PLAN_STEP_0X.md`.
6. Keep every `PLAN_STEP_0X.md` file at the same directory level as its owning `PLAN.md`.
7. Do not place step files in nested planning subdirectories.
8. Follow feature-module and module-layer links only when the planning document indicates that more ownership or placement detail is needed.

## Exit Condition

1. You have selected the planning document that matches the current planning stage.
2. The next read is [phases/BIG_PICTURE.md](phases/BIG_PICTURE.md), [../ddd/DDD.md](../ddd/DDD.md), or [phases/STEPS.md](phases/STEPS.md), depending on the plan state and domain-modeling impact.