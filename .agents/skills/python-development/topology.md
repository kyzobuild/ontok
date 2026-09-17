---
type: Reference
description: How TCA constructs compose through an acyclic dependency graph from semantic types to runtime boundaries. Read when placing code or choosing dependency direction.
---

# Topology

## Dependency Direction

| Construct | May depend on |
|---|---|
| Semantic scalar | Pydantic and its primitive or `StrEnum` value space |
| Value object | Semantic scalars, value objects, unions, collections |
| Concept model | Semantic scalars, value objects, concept models, unions, collections; authorization-bearing outcome facts may also derive actions over lower-level concepts |
| Union | Alternatives on one semantic axis; the union occupies its variants' dependency layer |
| Ordered union | Foreign models only |
| Collection | Members from its own layer or a lower semantic layer |
| Transformation | Semantic scalars, value objects, concept models, unions, collections, foreign models, contract models, actions, transformations |
| Action | Semantic scalars, value objects, concept models, immutable state-transition facts, unions, collections |
| State transition | Prior-state alternatives, additional semantic facts, and actions constructed by owned derivations |
| Foreign model | Semantic scalars, matching domain values or concepts, and nested foreign models, unions, or collections |
| Contract model | Semantic scalars, value objects, concept models, unions, collections |
| Config | Semantic scalars, value objects, `SecretStr`, and settings substrate |
| Route | Domain models whose meaning already matches ingress, foreign models, and contract models |
| Effect interpreter | Actions, foreign models, concept-model or union outcomes, and one imported non-program-owned capability |
| Composition root | The terminal construct, its declared input facts, configuration, and imported capabilities bound at interpreter fields |

The Python import graph is acyclic. A semantic type may refer recursively to itself or a forward-declared peer; every constructed runtime value remains finite and complete.

A successor fact may derive an action carrying that same fact. These declarations can share their domain module, with a forward return annotation for the derivation; no reciprocal Python imports or stored action/successor cycle is needed. Construction establishes the successor's fields before the derivation is read. A foreign-to-domain transformation depends on both representations only when their meanings actually differ; name or wrapper lifting remains nested construction.

## Placement

```text
domain/<context>/type.py              semantic scalars
domain/<context>/value.py             value objects and their unions or collections
domain/<context>/<concept>.py         concepts, transformations, actions, transitions,
                                     and their owned unions or collections
domain/<context>/api.py               contract models
integration/<system>/model.py         foreign models
integration/<system>/<meaning>.py     necessary foreign-to-domain transformations
integration/<system>/interpreter.py   effect interpreters
api/<context>.py                      routes
config.py                             config
main.py                               outer construction of the terminal meaning
```

Domain concept files are named for their domain meaning, including files containing transformations, actions, or transitions. Several declarations in a file do not justify `transformation.py`, `action.py`, or `transition.py`; place them with their owning domain concept. The established `type.py`, `value.py`, and `api.py` vocabulary and contract layers retain their stated roles.

Technology-pattern filenames are forbidden in the domain: `store`, `repository`, `handler`, `controller`, `manager`, `processor`, `router`, and `crud`. Dumping-ground names are also forbidden: `utils`, `helpers`, `common`, `misc`, and `shared`. A domain expert must recognize what the domain contains from the filename, not have to explain what the technology does. Declaration names follow the bans in [TCA](tca.md).

A union or collection is colocated with the layer of its variants or members. It never moves those dependencies to a higher or lower layer.

## Boundaries

- Domain constructs import no SDK, framework, environment, client, database, broker, filesystem, or subprocess capability.
- Foreign models contain no live client.
- Actions contain no interpreter, client, outcome, or mutable current-state reference; an immutable state value may be an effect input.
- State transitions are immutable successor facts, not procedures; they own any action authorization but no effect execution or current-state holder.
- Routes contain no domain decision.
- Effect interpreters contain no domain transition.
- The composition root is an outer construction expression, not a function or an additional wrapper type. It supplies no current-state slot, receive loop, transition loop, or orchestration procedure.
