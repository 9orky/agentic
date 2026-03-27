# Infrastructure Shim Rules

Document Class: leaf

## Purpose

Within the owning module's `infrastructure` layer, shim rules define what the layer shim and anchor shims expose to the rest of the module.

## Applies When

Read this file when the task affects `infrastructure/__init__.py`, an infrastructure anchor `__init__.py`, or any public export surface that other layers import.

## Ownership

Infrastructure shims own:

1. the minimal public export surface for infrastructure anchors
2. factory functions that build infrastructure services or adapters when callers need construction through the shim
3. stable type exports that application code or sibling infrastructure anchors must import through the public seam
4. concealment of private wiring details behind the shim boundary

## Core Rules

### Export Contract

1. Expose infrastructure symbols only through `infrastructure/__init__.py` or the owning anchor shim.
2. Export the minimum surface needed by application or sibling infrastructure consumers.
3. Keep private helpers, concrete wiring steps, and intermediate models behind the shim.
4. When a shim exists mainly to provide ready-to-use infrastructure services, prefer exporting factory functions for those services instead of leaking internal assembly steps.

### Factory Contract

1. A shim-level factory function should construct and return one meaningful infrastructure service or adapter.
2. Name factory functions by the concrete service or adapter they produce.
3. Keep composition details inside the shim or the owning anchor rather than spreading them across callers.
4. If many callers need different assembly choices, make the variation explicit in the factory contract rather than by deep-importing private parts.

## Constraints

1. Do not use the shim as a dumping ground for unrelated helper exports.
2. Do not force callers to deep-import private infrastructure files just to build a concrete adapter.
3. Do not move application workflow decisions into infrastructure factories.
4. Do not widen shim exports to preserve accidental callers.

## Acceptance Check

1. Cross-layer consumers import infrastructure only through the layer shim or owning anchor shim.
2. Shim exports stay minimal and intentional.
3. Factory functions are used when the shim's public responsibility is to provide a ready-to-use infrastructure service or adapter.
4. Private wiring remains hidden behind the shim boundary.