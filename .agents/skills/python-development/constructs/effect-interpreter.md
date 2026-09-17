---
type: Reference
description: How typed actions are executed through concrete external capabilities and observed outcomes are constructed. Read when binding effects to clients, storage, subprocesses, or transports.
---

# Effect Interpreter

## Use

Use when one typed action must be executed through one concrete external capability and its observed result must become a constructed outcome.

## Required Form

```python
class PersistPositionInterpreter(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
        arbitrary_types_allowed=True,
    )
    action: PersistPosition
    client: PositionClient = Field(exclude=True, repr=False)

    def execute(self) -> PositionPersisted:
        return PositionPersisted.model_validate(
            self.client.save(self.action.position.model_dump(mode="json"))
        )
```

`PositionClient` is the imported SDK capability. `PositionPersisted` is the program's concept model for the observed fact.

- Put the action and concrete capability in declared fields.
- Perform the external call only in `execute`.
- Serialize the action's semantic values at the client call.
- Construct a differing SDK reply as a foreign model, then construct the returned concept-model or union outcome.
- Translate every documented nonfatal capability failure into a constructed outcome variant.
- Propagate `CancelledError`, `KeyboardInterrupt`, and `SystemExit` to the invoking runtime.
- Leave programming defects uncaught.
- Use one interpreter type per action meaning.

## Do Not

- decide domain policy, construct a state successor, or become a receive/transition loop
- mutate the action or any domain value
- invent success before the external capability reports it
- catch broad exceptions, return flags, or collapse failure into absence
- hide retries whose repetition semantics are not declared by the action
- retain raw replies after the outcome constructs

## Prove

Execute against the real capability. For each documented success and nonfatal failure, assert the observed external change, serialized request, and exact concept-model or union outcome. Run one cancellation case and assert propagation. Inspect the module imports and method body to confirm no state-transition type or constructor appears.
