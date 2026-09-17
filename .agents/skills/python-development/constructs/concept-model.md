---
type: Reference
description: How a frozen complete domain thing or fact is constructed from declared meanings. Read when modeling a full concept, refinement, or durable fact.
---

# Concept Model

## Use

Use for one complete domain thing, durable fact, or genuine refinement of another concept. The class is the kind.

## Required Form

```python
class Fill(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    order_id: OrderId
    price: Price
    quantity: Quantity


class PartialFill(Fill):
    remaining: Quantity
```

- Fields are declared semantic relations to other constructs.
- Subclass only when every child is a kind of the parent.
- A refinement inherits every parent field, configuration, property, and semantic method unchanged; it only adds stricter facts. No program-owned custom validator is declared or inherited.
- Put enduring identity in its own semantic scalar field when the thing has identity.
- Keep completed facts frozen and recursively immutable.
- Derive facts implied by existing fields through a transformation.

## Do Not

- add `type`, `kind`, registry, or URI fields to simulate class identity
- subclass to reuse fields when the child is not a kind of the parent
- store a derived fact
- hold clients, resources, current state, or effect execution
- use `None`, `Optional`, or nullable fields instead of named constructed absence
- mirror a foreign or contract representation without distinct ownership

## Prove

Construct the full fact from its declared inputs and refuse each declared invalid boundary. Parse the full child declaration and MRO: reject additional bases, class keywords that alter configuration, redeclaration of any parent field, property, or semantic method, and any program-owned custom validator or construction hook; assert the resolved child `model_config` equals the parent's. Run the configured static checker on assignment of the child to the parent type. Round-trip through the known concrete class; use a genuine discriminated union when serialized subtype identity must survive a base-typed boundary.
