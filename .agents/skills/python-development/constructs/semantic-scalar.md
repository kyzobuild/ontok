---
type: Reference
description: How one admitted atomic meaning is constructed over a primitive or closed value space. Read when a value has independent identity, vocabulary, units, or constraints.
---

# Semantic Scalar

## Use

Use for one atomic program meaning whose value space is primitive, constrained primitive, or closed vocabulary. If the value has no independent meaning, keep it inside its owning construct.

## Required Form

```python
class Price(RootModel[Decimal]):
    model_config = ConfigDict(
        frozen=True,
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    root: Decimal = Field(gt=0, decimal_places=8)


class Side(StrEnum):
    BUY = "buy"
    SELL = "sell"
```

- Use frozen `RootModel[P]` when the meaning wraps a primitive.
- Use `StrEnum` when the meaning is exactly a closed string vocabulary.
- Put every bound in `Field`; an open range has a docstring stating that every primitive value is valid.
- Pass the scalar itself across semantic boundaries. Read `.root` only inside a transformation, route, interpreter, or composition root that immediately consumes the primitive.

## Do Not

- use the same scalar type for values with different meanings
- create a scalar for an incidental primitive
- use a bare primitive where a semantic scalar is required
- wrap a `StrEnum` again unless the wrapper adds a different meaning
- branch to enforce a bound after construction

## Prove

For each existing `Field` bound, test the bound itself according to its inclusive or exclusive declaration. Construct one representative admitted value and refuse one representative value from each excluded side. Assert the root runtime type, ordinary assignment rejection, and JSON reconstruction equality. When the scalar serves as a key, additionally prove consistent equality and hashing; a wire-key encoding must be injective over admitted keys and round-trip through the declared key constructor. Successful key serialization does not prove the enclosing [collection](collection.md) immutable or establish its source duplicate policy.
