# Domain Isolation Rule

Code existing within the Domain layer is the core of our business logic.

**CRITICAL RULE:**
- `src/domain` modules MUST NOT import from `src/infrastructure` or `src/ui`.
- All interactions with the outside world must be handled via dependency-injected interfaces.
