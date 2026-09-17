---
type: Playbook
description: How to select exactly one of the 15 TCA constructs or no construct. Read before introducing any program structure.
---

# Construct Selection

For every proposed declaration, name the program-owned meaning first, then select exactly one row. If no row matches, the meaning has not been articulated and the declaration is not written.

| Meaning | Construct |
|---|---|
| One atomic meaning over a primitive or closed value space | [Semantic scalar](constructs/semantic-scalar.md) |
| Descriptive or measured product whose meaning is exhausted by field equality | [Value object](constructs/value-object.md) |
| Full domain thing, refinement, or durable fact | [Concept model](constructs/concept-model.md) |
| Closed alternatives on one semantic axis | [Union](constructs/union.md) |
| Overlapping foreign alternatives with intentional attempt order | [Ordered union](constructs/ordered-union.md) |
| Sequence or association with collection-level meaning | [Collection](constructs/collection.md) |
| Pure implication from proven inputs to a constructed output | [Transformation](constructs/transformation.md) |
| Another system's differing representation | [Foreign model](constructs/foreign-model.md) |
| This program's published request or reply | [Contract model](constructs/contract-model.md) |
| Environment and deployment input | [Config](constructs/config.md) |
| One outer construction of the terminal meaning | [Composition root](constructs/composition-root.md) |
| Transport ingress and egress | [Route](constructs/route.md) |
| Execution of a typed action through an external capability | [Effect interpreter](constructs/effect-interpreter.md) |
| New immutable state fact containing prior state and additional facts | [State transition](constructs/state-transition.md) |
| Description of one intended external effect | [Action](constructs/action.md) |

## Sorting Laws

- A uniform closed vocabulary is a semantic scalar; alternatives with different facts form a union.
- A value object is exhausted by field equality; an independently referable thing, occurrence, or durable fact is a concept model.
- A plain tuple field is not a collection unless the collection itself has meaning.
- Matching foreign and domain meaning constructs the domain type directly. Differing names and nesting use foreign annotations and aliases; an actual semantic conversion requires a foreign-to-domain transformation.
- Publishing a domain model directly does not reclassify it as a contract model; create a contract model only for a distinct published projection.
- Construction refusal is not an ordered-union domain outcome.
- A successor whose fields establish its relationship to prior state is the state-transition form, not a concept model plus a separate verb-shaped wrapper. It owns any effect authorization; an action describes the effect; an interpreter performs it. The composition root supplies no domain policy or state-management procedure.
