---
type: Reference
description: How overlapping foreign alternatives are constructed by explicit tested precedence. Read when external input has no reliable discriminator and attempt order is intentional.
---

# Ordered Union

## Use

Use only at a foreign boundary when one untagged input can inhabit overlapping foreign shapes and the source contract defines which construction wins.

## Required Form

```python
ForeignReply = Annotated[
    DetailedReply | SummaryReply,
    Field(union_mode="left_to_right"),
]
ForeignReplyConstructor = TypeAdapter(ForeignReply)
```

- Order variants from the source-defined strongest interpretation to the source-defined fallback.
- Give every variant a frozen Pydantic shape.
- Capture declared foreign exceptions as explicit foreign models before construction.
- Keep the `TypeAdapter` beside the alias and name it for that alias.
- Treat all undeclared failures as failures, not fallback input.

## Do Not

- use attempt order for domain decisions
- use an ordered union when data carries a reliable discriminator
- use coercion accidents to define precedence
- catch `ValidationError` to manufacture a default, partial value, or domain refusal
- place a catch-all model last to hide unknown foreign changes
- introduce a program-owned custom validator for parsing, selection, or any other purpose

## Prove

Construct one source-contract witness unique to each variant. For every pair of overlapping variant schemas, construct one source-contract witness accepted by both and assert that the earlier variant wins. Construct one value rejected by all variants. Repeat the matrix against the installed Pydantic version.
