---
type: Reference
description: How this program's request or reply contract is constructed and serialized. Read when defining a program-owned external interface.
---

# Contract Model

## Use

Use when this program owns a published request or reply whose shape is not already the exact owned domain meaning being published.

## Required Form

```python
class OrderRequest(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    product_id: ProductId
    side: Side
    quantity: Quantity
    limit: Price
```

- Compose contract fields from declared semantic types.
- Construct requests at the route before anything consumes them.
- Construct replies from proven domain facts or observed outcomes.
- Put an alias on a field only when this program deliberately owns that published wire name.
- Put a derived field in serialization only through `@computed_field` returning an explicitly constructed value.
- Publish the domain model directly when ownership, meaning, shape, and evolution policy are identical; direct publication does not make it a contract-model construct.

## Do Not

- treat another system's shape as this program's contract
- duplicate a domain model merely to create a DTO layer
- serialize with ad hoc `include`, `exclude`, or field-copying dictionaries
- expose a foreign client, exception, or raw representation
- let a route add or remove semantic fields

## Prove

Construct each declared request boundary and refuse each field's invalid boundary. Serialize every reply variant with declared aliases. Reconstruct input with `round_trip=True, by_alias=True` when aliases exist, then assert exact published names and computed wire values separately.
