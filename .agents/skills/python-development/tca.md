---
type: Reference
description: The executable-ontology principle, one-to-one correspondence, and four TCA breaks. Read before applying the construct whitelist.
---

# Type Construction Architecture

## Standard

Meaning lives in program structure; construction is its proof. The program is an executable ontology: types name meanings, fields name relations, constructors prove facts, transformations express implications, successor facts contain their prior facts, and actions state intended effects.

Every declaration is exactly one of the 15 constructs in [construct selection](construct-selection.md). No sixteenth construct, generic helper layer, or procedural substitute is allowed.

## Correspondence

- Every program-owned meaning has exactly one structural home.
- Every structure carries exactly one program-owned meaning.
- The class is the kind; refinement uses subclassing, not a `type`, `kind`, registry, or URI field.
- A boundary representation is distinct only when its owner or semantics are distinct.
- A derived fact has one source and is never stored beside that source.
- A name states the domain thing, fact, relation, transformation, transition, or action carried by the structure.

## Four Breaks

- **Escaped:** a meaning exists only in prose, primitive usage, procedure, ordering, or convention.
- **Duplicated:** one meaning has two independently maintained structures.
- **Vacuous:** a structure exists without a program-owned meaning.
- **Fused:** one structure carries meanings that vary independently.

Every implementation ends with all four checks. A failed check changes the model; documentation cannot waive it.

## Naming

Name every structure for the domain thing or fact it carries, never a pipeline stage, data direction, or processing step. Banned names and generic suffixes: `Record`, `Item`, `Data`, `Payload`, `Result`, `Entry`, `Info`, `Handler`, `Manager`, `Processor`, `Incoming`, `Outgoing`, `Processed`, `Enriched`, and the `Event` suffix. A domain expert must recognize the thing without describing the data flow. Domain filenames follow the same rule in [topology](topology.md).

## Program Forms

Semantic values are Pydantic models. `StrEnum`, `Literal`, `SecretStr`, Pydantic union aliases, and `TypeAdapter` are substrate forms used inside whitelisted constructs. Existing objects supply the facts from which new objects construct. There is no mutable consistency exception, program-owned runner, or separate validation machinery.

Domain execution is a dependency graph of constructed values, never procedural orchestration. A frozen model does not admit an arbitrary procedure inside a method or property. Derivations use the closed one-expression [transformation](constructs/transformation.md) algebra; union variants own their differing behavior; facts own the effects they authorize. Semantic absence is constructed, never `None`.

A function that calls everything in order means the terminal object has not been named: name it and construct it. Do not rename that function as a model, a callback chain, or a generic engine. Imported capabilities perform external effects at their declared boundary; they are not permission to restore a domain procedure.
