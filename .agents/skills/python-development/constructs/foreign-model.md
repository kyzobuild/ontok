---
type: Reference
description: How another system's representation is lifted into a frozen typed boundary model. Read when foreign shape or vocabulary differs from the program's meaning.
---

# Foreign Model

## Use

Use when another system owns a representation whose names, nesting, omission, or value meanings differ from this program's domain model.

## Required Form

```python
class VenueFill(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    order_id: OrderId = Field(alias="ordId")
    price: VenuePrice = Field(alias="px")
    quantity: VenueQuantity = Field(alias="qty")
```

- Name the model for the foreign thing and place foreign keys in aliases.
- Use nested annotations for nested source structure; reuse domain types where meaning and shape agree, and use nested foreign models only where they differ.
- Use `validation_alias`, `AliasPath`, `model_validate_json`, and `from_attributes=True` to lift the source whole.
- Model every source field the program consumes and no unconsumed field.
- Use source-owned scalar meanings when the source's semantics differ.
- Lift names and nesting through annotations and aliases, not a field-copying transformation. When the value meanings already agree, nested domain annotations construct those meanings directly.
- Construct a [transformation](transformation.md) only for an actual semantic conversion, such as source quantities in a different unit. State that conversion and express it within the closed derivation algebra; a separate `FillLift` is not justified by crossing the boundary alone.
- Set `extra` to the source contract: forbid closed input and ignore only fields the source explicitly permits consumers to ignore.
- Serialize an alias-bearing source representation with `by_alias=True`; `validation_alias` and `AliasPath` do not define output names.

## Do Not

- copy foreign vocabulary into a domain concept
- keep raw dictionaries or SDK objects after the foreign model constructs
- read fields again from the source object
- introduce any program-owned custom validator; annotations and aliases express construction
- hold a live client or resource
- create a foreign model when the domain model already matches the source meaning and shape
- create a transformation to repeat construction already expressed by annotations, aliases, or `from_attributes=True`

## Prove

Capture one whole unedited source reply for each documented source variant. Construct each reply, assert every consumed nested runtime class, and replace each consumed field once with a malformed value to assert its error location. For each separate conversion, identify the changed meaning and prove that it is not merely name, wrapper, or attribute lifting already handled by construction. Assert alias-key output separately with `by_alias=True` when the source supports output.
