# ONTOK Semantic Topology

## Purpose

Add Semantic Topology to ONTOK Core as the system by which Concepts form an evolving organizational structure of meaning.

ONTOK already provides the primitives required to represent organizational structure, reality, agency, meaning, and governance. `Concept` provides meaning and alignment at the level of an individual declaration. Semantic Topology provides the missing structure among Concepts themselves.

The distinction is:

> Core lets an organization declare structure and meaning. Semantic Topology lets it organize and reconcile meaning across independent declarations.

Semantic Topology is not a new primitive. The ONTOK kernel remains exactly twelve primitives:

```text
Node
Connection
Entity
Relation
State
Event
Role
Goal
Action
Concept
Context
Rule
```

Semantic Topology is composed from them.

## Architectural Position

A Semantic Topology is a durable organizational structure built primarily from:

* `Concept`
* specialized `Relation` classes between Concepts
* `Context` where a semantic relationship is conditional
* an `Entity` representing the topology as a persistent organizational artifact

The topology belongs to the organization, not to any particular graph database, application, language model, ontology vendor, or source system.

It is an overlay on the organizational graph, not a replacement for that graph.

## Concept

Do not reintroduce type identity into `Concept`.

The class is the kind throughout ONTOK. `Concept` concerns meaning and alignment: what a declaration means and how that meaning corresponds to another meaning.

Examples include the organizational understanding that:

```text
cust_no means Customer
Member corresponds to Customer
Payment is close to Transaction
```

The exact representation of declaration-to-Concept alignment should be modeled as part of `Concept`; Semantic Topology should not solve that problem by introducing `TypeId`, string tags, or an instance-level kind field.

## SemanticTopology

Add a Core construct representing one organization's current semantic topology.

Conceptually:

```python
class SemanticTopology(Entity):
    revision: TopologyRevision
    concepts: frozenset[Concept]
    relations: frozenset[SemanticRelation]
```

`SemanticTopology` is an `Entity`, not a primitive. Its identity persists while its contents evolve.

`TopologyRevision` is a positive monotonic revision number. ONTOK models are immutable, so a topology evolves by producing a new valid representation with the same topology identity and a later revision.

The topology should remain usable as an ordinary Pydantic object by pipelines, query systems, graph adapters, agents, synchronization processes, and other software.

## Semantic Relations

Semantic relationships are specialized `Relation` classes. Do not add a `relation_type` or other discriminator field. The class is the kind.

Define a common semantic relation refinement whose endpoints are Concepts:

```python
class SemanticRelation(Relation):
    source: Concept
    target: Concept
```

Concrete semantic relationships should initially remain deliberately small.

### Equivalent

Two Concepts express the same meaning for purposes of the topology.

```text
Customer ← equivalent → Member
```

Semantics:

* symmetric
* transitive
* does not merge or destroy either Concept identity

### Broader

The source Concept is semantically broader than the target.

```text
FinancialAccount → broader → CheckingAccount
```

Semantics:

* directional
* irreflexive
* the broader graph must remain acyclic
* transitive closure may be derived
* `narrower` is the inverse view and does not need to be stored as a second Relation

### Related

The Concepts have a meaningful associative relationship without asserting equivalence or hierarchy.

Semantics:

* symmetric
* non-transitive

### CloseMatch

The Concepts are sufficiently similar to be useful for mapping or retrieval but are not safe to treat as equivalent.

Semantics:

* symmetric
* non-transitive
* weaker than `Equivalent`

### Overlap

The Concepts share part of their meaning while each retains meaning not contained by the other.

Semantics:

* symmetric
* non-transitive
* does not imply a broader/narrower relationship

These relations are the initial ONTOK semantic vocabulary, not an assertion that no additional semantic Relation subclasses may ever exist. Modules and organizations may refine the model where their domains require stronger semantics.

## Context

A semantic relationship may be true only under particular organizational conditions.

Semantic relations should therefore be able to carry an optional `Context` when required.

For example:

```text
Member equivalent Customer
    within RetailBankingContext
```

does not require the organization to claim universal equivalence between those Concepts.

Absence of a Context means the relationship is asserted generally within the scope of that topology.

## Topology Invariants

A valid Semantic Topology must satisfy at least these invariants:

1. Every member of `concepts` is a `Concept`.
2. Every member of `relations` is a semantic `Relation` whose source and target are Concepts contained in the topology.
3. No semantic relation may use a non-Concept endpoint.
4. `Broader` may not be reflexive.
5. The directed `Broader` graph must be acyclic.
6. Symmetric relations have symmetric semantics even if the implementation stores only one canonical edge.
7. `Equivalent` does not collapse Concept identity.
8. Absence of a relationship means unknown or undeclared, not false.
9. A model-generated proposal does not become authoritative merely because a model produced it.
10. Local representations remain legitimate after alignment; topology does not rewrite originating systems.

Validation should protect the semantic invariants without attempting to predefine an organization's concepts.

## Evolution

Semantic Topology is intentionally evolutionary.

Organizations introduce systems, retire systems, change policies, split concepts, merge operating distinctions, acquire companies, change terminology, and discover previously implicit structure. The topology must be able to reflect that change without being rebuilt from scratch.

The lifecycle is:

```text
observe
  ↓
discover or infer candidate structure
  ↓
construct proposed ONTOK declarations
  ↓
validate
  ↓
accept, reject, or revise
  ↓
publish next topology revision
  ↓
continue observing
```

A revision may:

* add a Concept
* stop recognizing a Concept
* add or remove a semantic Relation
* replace one semantic relationship with another
* add or remove Context
* split one Concept into several
* establish equivalence among previously separate Concepts
* withdraw an equivalence when meanings diverge

Concept identity should remain stable when the meaning itself remains stable. Relationships may evolve around that Concept.

ONTOK Core does not need a dedicated primitive for topology-change history. Because the topology is part of the organizational graph, organizations may memorialize meaningful topology changes through `Event` refinements when durable history is required.

## Emergence

Semantic Topology must not require a top-down enterprise taxonomy.

It should be constructible from the organization that already exists. Candidate Concepts and relationships may be discovered from:

* ONTOK graphs
* application classes
* database schemas
* knowledge graphs
* APIs
* events
* documents
* policies
* external ontologies
* operating language
* other structured or unstructured sources

Deterministic software may establish mappings where the semantics are mechanically known. Models may propose mappings where interpretation is required. Humans or organizational policy may participate where authority requires them.

ONTOK represents the result consistently regardless of who or what discovered it.

## Models and Software

Semantic Topology is designed for mixed deterministic and probabilistic programs.

Language models are appropriate for bounded semantic inference such as:

* concept discovery
* schema interpretation
* candidate alignment
* broader/narrower inference
* detecting possible semantic drift
* explaining differences
* classifying new declarations

Software retains responsibility for:

* orchestration
* validation
* durable state
* topology revision
* authorization
* application of organizational rules
* persistence
* propagation to dependent systems

Models infer. Software governs.

## Relationship to External Systems

A Semantic Topology may reconcile meanings from systems that use entirely different representation technologies.

For example:

```text
AWS Neptune                 Microsoft Fabric

Customer                    Member
Account                     FinancialAccount
Transaction                 Payment
Merchant                    Counterparty
```

An ONTOK topology may represent:

```text
Customer        Equivalent      Member
FinancialAccount Broader        Account
Transaction     CloseMatch      Payment
Merchant        Overlap         Counterparty
```

Neither source model becomes canonical. ONTOK preserves the local meanings and declares their organizational relationship.

## SKOS Interoperability

Use SKOS as an interoperability model where it fits, not as the ONTOK programming surface.

Natural mappings include:

```text
ONTOK Concept          ↔ skos:Concept
SemanticTopology       ↔ skos:ConceptScheme
Broader                ↔ skos:broader
Related                ↔ skos:related
Equivalent             ↔ skos:exactMatch
CloseMatch             ↔ skos:closeMatch
```

`Overlap` may remain an ONTOK-specific semantic Relation unless a better interoperable representation is chosen.

ONTOK should be able to serialize or project Semantic Topology into SKOS-compatible RDF, but Python users should not need to program directly against SKOS classes to use ONTOK.

## What Semantic Topology Is Not

Semantic Topology is not:

* a thirteenth ONTOK primitive
* a universal classification tree
* an enterprise canonical schema
* a requirement that equivalent Concepts share one identifier
* a master data management system
* an LLM-owned knowledge structure
* a replacement for domain ontologies
* a requirement that source systems adopt ONTOK internally

It is the organizational structure that makes independently declared meaning navigable, comparable, and interoperable.

## Python Surface

The intended developer experience should remain small.

Conceptually:

```python
from ontok.core import (
    Concept,
    SemanticTopology,
    Equivalent,
    Broader,
    Related,
    CloseMatch,
    Overlap,
)
```

An application should be able to construct, validate, query, serialize, and revise a topology using normal Python objects.

Do not introduce generic `kind`, `type`, or URI discriminator fields to simulate subclassing. ONTOK uses the class as the kind.

## Specification Placement

Semantic Topology belongs in the **Meaning** portion of `ontok-core`.

The implementation-independent Core specification should define:

* `SemanticTopology`
* `TopologyRevision`
* `SemanticRelation`
* `Equivalent`
* `Broader`
* `Related`
* `CloseMatch`
* `Overlap`
* their invariants and derivable semantics

The Python realization should implement the same semantics under `ontok.core`.

This changes ONTOK Core's capabilities without changing its twelve-primitive kernel.

## Completion Criterion

Semantic Topology is complete when ONTOK can represent an organization's evolving conceptual structure without requiring local systems to share classes or schemas, validate the topology's semantic invariants, revise that topology over time, expose it as ordinary program data, and project it into interoperable semantic representations such as SKOS when required.

At that point ONTOK can represent not only organizational declarations and their meanings, but also the structure of meaning that emerges across the organization.
