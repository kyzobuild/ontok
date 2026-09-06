---
name: python-development
description: The construct standard for all Python code in this repo — Type Construction Architecture (TCA) every meaning gets exactly one structure, every structure carries exactly one meaning, and construction is the proof. Use when writing, reviewing, or refactoring any Python code. Covers the 15 constructs, the four breaks, naming, construction discipline, and substrate verification.
---

# Python Development

One principle: a value's existence is the evidence its constraints held — an illegal value cannot be built.

**Domain execution is a dependency graph of constructed values, never procedural orchestration.**

## The four breaks

Run this test before finishing any code. Name the break or there is none.

- **escaped** — a meaning with no structure: a constraint in a comment, a check in a procedure, a convention the type does not carry
- **duplicated** — a meaning in more than one structure: a rule restated across layers, one fact in two fields
- **vacuous** — a structure with no meaning: a type minted to save repetition, a name that says nothing
- **fused** — a structure with more than one meaning: several domain axes in one field or label set

## Naming

Name every structure for the domain thing or fact it carries — never a pipeline stage, a data direction, or a processing step. Banned: `Record`, `Item`, `Data`, `Payload`, `Result`, `Entry`, `Info`, `Handler`, `Manager`, `Processor`, `Incoming`, `Outgoing`, `Processed`, `Enriched`, and the `Event` suffix. Test: a domain expert recognizes the thing named, without describing the data flow.

## Construction discipline

- Construction replaces validation: a value that fails construction does not exist as a domain value.
- Never check a value after construction, never move an unproven value forward, never store, pass, or branch on unmodeled data.
- No module-level functions; every operation belongs to the semantic structure that owns its inputs and result.
- No module-level domain values, registries, configuration, caches, clients, or `SCREAMING_SNAKE_CASE` constants; globals are meaning without an owning structure.
- A domain fact implied by a model's fields is a derivation on that model, never a free function.
- Never sequence domain work in a function, handler, processor, manager, pipeline, or orchestrator — the dependency graph between constructed values determines construction order.

## Route the thing you are building

- one atomic value → [semantic scalar](semantic-scalar.md)
- a small value, no identity → [value object](value-object.md)
- a full domain thing or fact → [concept model](concept-model.md)
- a choice on one axis → [union](union.md)
- foreign data, no identity, may fail → [ordered union](ordered-union.md)
- a sequence with its own meaning → [collection](collection.md)
- a fact of a model's fields, or a question with an input → [derivation](derivation.md)
- another system's shape → [foreign model](foreign-model.md)
- this program's API shape → [contract model](contract-model.md)
- environment values → [config](config.md)
- the entrypoint → [composition root](composition-root.md)
- transport ingress → [route](route.md)
- binding clients to the model → [binding](binding.md)
- live state plus clients → [consistency model](consistency-model.md)
- a state transition → [verb](verb.md)

## Substrate claims

A claim about Pydantic construction behavior requires a substrate run; a claim about gate coverage requires a gate run; a claim about basedpyright behavior requires a basedpyright run. Never add doctrine from analogy, idiom, or common Python practice.

All exemplars share one domain — venue fills, positions, and orders — and are correct to copy verbatim.
