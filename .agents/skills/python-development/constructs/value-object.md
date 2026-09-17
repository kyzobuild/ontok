---
type: Reference
description: How a frozen identityless product is constructed and compared by value. Read when a descriptive or measured meaning is exhausted by its field values.
---

# Value Object

## Use

Use for one descriptive or measured meaning with no identity, occurrence, lifecycle, or independent reference beyond its fields. Equality of all fields exhausts its meaning.

## Required Form

```python
class Spread(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    bid: Price
    width: SpreadWidth

    @property
    def ask(self) -> Price:
        return Price(self.bid.root + self.width.root)
```

- Every field is a semantic scalar, value object, union, or collection; a reference to an identified concept is its identity scalar, not the concept model.
- Store the independent parameters and derive every implied fact.
- Reparameterize a cross-field relation so invalid combinations have no representation.
- Represent meaningful absence or distinct alternatives by named union variants, never nullable fields.

## Do Not

- add an identity field
- store a derived field beside its source fields
- use a mutable constituent
- hold a client, resource, action interpreter, or current-state pointer
- replace the value object with an anonymous tuple or dictionary

## Prove

Construct one product at every constituent boundary. Identify how its parameterization establishes each product invariant and test excluded input at that structural boundary, not through a custom validator. Assert field equality, reject ordinary field assignment, inspect every nested annotation for immutable types, and assert JSON reconstruction equality.
