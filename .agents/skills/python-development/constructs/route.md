---
type: Reference
description: How transport ingress constructs typed input and projects declared output. Read when implementing an HTTP, CLI, message, stream, or framework entrypoint.
---

# Route

## Use

Use where a transport representation enters or leaves the program. A route is a frozen Pydantic model whose construction completes one transport crossing.

## Required Form

```python
class FillRoute(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    fill: Fill = Field(
        validation_alias=AliasPath("data", "payload")
    )

    @classmethod
    def receive(cls, raw: str) -> "FillRoute":
        return cls.model_validate_json(raw)


class FillReplyRoute(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    reply: FillReceipt

    def emit(self) -> str:
        return self.reply.model_dump_json(by_alias=True)


route = FillRoute.receive(raw)
```

- Construct exactly one route from the whole transport representation.
- Let the route's annotated domain, foreign, or contract field recursively construct the ingress value. Here `data.payload` already has the domain `Fill` shape and meaning; a foreign model or lift would duplicate that construction.
- Expose that constructed field to the transformation, transition, or interpreter that consumes it.
- Use a separate egress route owning exactly one constructed outbound contract.
- Expose `receive` as the callback registered with an imported framework; no wrapper function is added.
- Keep authentication extraction, status codes, headers, and protocol framing inside the route when they are transport facts.

## Do Not

- decide domain policy
- construct a successor state
- execute an action
- hold current state or a concrete client
- parse fields by hand when Pydantic's declared construction graph expresses the transport
- pass transport wrappers into domain constructs
- perform a domain transformation
- assemble reply dictionaries or selectively include/exclude semantic fields

## Prove

Call `receive` with one captured transport string and one malformed value for each consumed field. Assert the nested runtime class and error location. Construct the egress route with each reply variant, call `emit`, and compare parsed JSON values; compare UTF-8 bytes separately only when byte identity is contractual.
