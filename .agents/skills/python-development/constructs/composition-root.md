---
type: Reference
description: How one outer construction composes the declared program at its boundary. Read when defining an entrypoint or binding constructed facts to an imported capability.
---

# Composition Root

## Use

Use at the program boundary to construct the terminal meaning from its declared dependencies. The composition root is the outer construction expression, not a runner function, a mutable holder, or an additional model wrapping the program.

## Required Form

```python
PersistPositionInterpreter(
    action=Position(prior=prior, fill=fill).persistence,
    client=client,
)
```

`prior` and `fill` are existing facts; `client` is the imported capability supplied at the boundary. `Position` constructs the new fact without changing either input. Its `persistence` derivation constructs the authorized action. The outer interpreter binds that action to its capability. There is no separately maintained current position or sequence of domain steps.

Construction binds an effect interpreter; it does not execute an external effect. The invoking framework or caller uses the interpreter's declared boundary operation. Process lifetime, connection lifetime, and transport delivery belong to the imported runtime, not a program-owned replacement runner.

- Name the terminal meaning and construct it; let its annotated dependencies construct inside the outer call.
- Pass already constructed inputs directly. Do not copy their fields or reconstruct their identity.
- Keep configuration in its declared settings model and capabilities at their concrete interpreter fields.
- Express domain dependencies in fields and owned derivations, not statement order.
- Bind the declared concrete interpreter without class tests, callback registries, or a dispatch table.
- Use the existing terminal construct as the root; do not add a wrapper merely to represent execution.

## Do Not

- define a program-owned `run`, `main`, receive loop, state-advancement loop, or orchestration function
- move that procedure into a model method, property, constructor hook, callback chain, or custom validator
- introduce a mutable consistency holder or a local/global current-state reference to re-point
- create a runner, pipeline, manager, service, graph registry, or step list
- supply domain policy through construction order, action selection, or action filtering
- execute an effect in a constructor or pretend that constructing an interpreter performs its effect
- discard a domain-relevant observed outcome; it is a fact for the next declared construction, not a flag for a runner

## Prove

Construct the terminal object from declared inputs and inspect the resulting nested runtime types. Assert that the prior facts remain unchanged and that the action refers to the newly constructed fact. Confirm that construction makes no external call. Inspect the root for one construction expression and no runner, state assignment, callback orchestration, or custom construction hook. Test the interpreter's boundary operation separately; its observed outcome must construct through its declared type.
