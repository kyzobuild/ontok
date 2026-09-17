---
type: Reference
description: How a frozen typed value describes one intended external effect without executing it. Read when an effect request must be inspected, routed, persisted, retried, or interpreted.
---

# Action

## Use

Use when a constructed domain decision authorizes one external effect that must travel independently of its execution.

## Required Form

```python
class PersistPosition(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    position: Position
```

- Name the intended effect, not its handler, client, transport, or eventual outcome.
- Carry every semantic input required to request the effect.
- Add an idempotency or repetition key only when repeated execution is part of the effect contract.
- Keep the action frozen and recursively immutable.
- Let the authorizing domain fact construct it. When authorization follows succession, the successor fact owns that derivation; no transition procedure or policy in the composition root is needed.
- Place related effect alternatives in a union when one interpreter consumes a closed action family.

## Do Not

- execute the effect
- hold a client, resource, mutable current-state reference, retry loop, exception, or observed outcome; a completed immutable state value may be an effect input
- represent an event that already happened
- represent ordinary domain input that requests no external effect
- add transport serialization or foreign vocabulary
- claim success from the action's construction

## Prove

Construct one complete action, omit each required field once, and supply each field's invalid boundary once. Assert equality, reject ordinary assignment, inspect nested annotations for immutable types, and assert interpreter-owned serialization separately. Serialization does not reclassify the action as a contract model.
