---
type: Reference
description: How a new immutable state fact constructs from prior facts. Read when representing succession without mutation or procedural state management.
---

# State Transition

## Use

Use when a new fact contains the relationship between prior state and an additional fact. The constructed object is the successor, not a command to change an existing object. Its fields establish the transition; no consistency holder or transition procedure is required.

## Required Form

```python
class FlatPosition(BaseModel):
    """The opening position contains no fills."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )


class Position(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    prior: "FlatPosition | Position"
    fill: Fill

    @property
    def persistence(self) -> "PersistPosition":
        return PersistPosition(position=self)


PositionState = FlatPosition | Position
```

`Position(prior=previous_position, fill=fill)` is the complete transition construction. Its `Fill` annotation also constructs a nested input representation; there is no separate lift or staged construction. `FlatPosition` is the opening concept, `Position` is the successor fact, and `PositionState` is their union. A later position may contain this position as its prior fact; neither object is overwritten.

Here the new position authorizes persistence: its owned derivation constructs the [action](action.md), not an observed success. The action declaration and this fact can live in the same domain module; the return annotation is forward-declared, and the derivation is read only after the declarations are complete. Constructing either fact performs no I/O.

- Put the prior fact and the additional facts in the successor's declared fields.
- Model compatible alternatives in those field types; do not accept arbitrary pairs and check them afterward.
- Construct the successor directly. Do not add a verb-shaped model whose only purpose is to call the successor's constructor.
- Derive implied facts on their owner through the closed [transformation](transformation.md) algebra.
- Keep any effect authorization on the fact that establishes it; the interpreter alone executes the effect.
- Preserve every predecessor. Succession is a relation between immutable values, not a mutable slot pointing at the latest one.

## Do Not

- own, mutate, or advance a current-state holder or reference
- hold or call a client, repository, cache, clock, random source, or environment
- perform persistence, publication, logging, retry, or serialization
- delegate action authorization to a caller or a separately selected transformation
- use `model_copy(update=...)`
- represent a transition rule as procedural branching inside or outside the transition model
- publish a successor before its construction completes
- introduce a custom validator, constructor override, or `model_post_init` to enact the transition
- store a duplicate successor beside the inputs that determine it

## Prove

Construct an opening fact, a successor from it, and a further successor from the first. Assert exact nested types, predecessor identity and unchanged contents, and reconstruction through the declared state union. Supply malformed nested input and assert that no successor is produced. Reject field assignment at every level. Read the authorized action and assert that it refers to its owning fact without performing an effect. Inspect declarations for no custom validators, construction hooks, verb-shaped intermediary, mutable holder, or procedure sequencing the transitions.
