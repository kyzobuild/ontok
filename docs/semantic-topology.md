# ONTOK Semantic Topology

## Purpose

ONTOK Semantic Topology (`ontok-st`) represents the evolving structure of meaning across an organization.

ONTOK Core lets software declare organizational kinds and construct facts using a small semantic kernel. Those declarations can evolve independently across applications, graphs, data platforms, APIs, documents, operating models, and external systems.

That independence is useful. It also creates a second-order problem.

Two systems can model the same organizational reality correctly while using different names, boundaries, relationships, and levels of abstraction:

```text
AWS Neptune                 Microsoft Fabric

Customer                    Member
Account                     FinancialAccount
Transaction                 Payment
Merchant                    Counterparty
```

The organization does not necessarily need one model to replace the other.

It needs to know how their meanings relate.

**Semantic Topology is the organizational structure that makes independently developed meaning explicit, comparable, navigable, and interoperable without requiring those local models to become one canonical ontology.**

It is a capability built from ONTOK Core, not an additional Core primitive.

---

## Architectural position

ONTOK Core contains thirteen primitives:

```text
Structure
  Node
  Connection

Reality
  Entity
  Relation
  State
  Event

Agency
  Role
  Goal
  Action
  Work

Meaning
  Concept
  Context

Governance
  Rule
```

Semantic Topology does not enlarge this kernel.

It composes Core primitives into an application-level semantic capability in the same way that other ONTOK modules compose Core into capabilities for execution, value streams, identity, or domain-specific concerns.

Its primary components are:

* `Concept` for organizational meaning
* specialized `Relation` classes between Concepts
* `Context` where a semantic assertion is conditional
* `SemanticTopology` as the persistent organizational identity of a topology
* `SemanticTopologyState` as an immutable state of that topology
* `Event` refinements that memorialize creation and revision

The topology belongs to the organization.

It does not belong to a graph database, cloud provider, language model, application, ontology vendor, or source system.

It does not replace the semantic models those systems already contain.

It describes how their meanings relate.

---

## Concept

`Concept` represents organizational meaning.

Semantic Topology operates on Concepts without turning them into surrogate type identifiers.

The ONTOK rule remains:

> **The class is the kind.**

Do not introduce `TypeId`, generic `kind` fields, string discriminators, class-name registries, or URI fields whose purpose is to recreate the language's type system inside its data model.

A Concept may represent meanings such as:

```text
Customer
Member
Payment
Transaction
ActiveEmployee
AuthorizedApprover
```

Two Concepts can remain distinct even when the organization determines that they are equivalent for some purpose.

That distinction is essential.

```text
Customer ───── equivalent ───── Member
    │                               │
    └──── identities remain ────────┘
```

Semantic alignment does not collapse Concept identity.

### Relationship to declarations

Semantic Topology does not define a universal mechanism for referencing arbitrary language-level classes.

A source system, adapter, or ONTOK module may expose the meaning of its declarations as Concepts and may model provenance or binding using ordinary ONTOK components appropriate to that source.

For example, an adapter for a graph ontology may expose Concepts corresponding to that ontology's declared business concepts. Another adapter may do the same for an application schema.

ST operates on the resulting Concepts.

It must not solve source binding by weakening the class-as-kind model.

---

## SemanticTopology

A semantic topology has persistent organizational identity.

```python
class SemanticTopology(Entity):
    """An organizational structure of related meaning."""
```

The topology itself is not a mutable container.

Its composition at a point in its evolution is represented by an immutable State.

```python
class SemanticTopologyState(State):
    """One complete published state of a SemanticTopology."""

    topology: SemanticTopology
    revision: TopologyRevision
    concepts: frozenset[Concept]
    relations: frozenset[SemanticRelation]
```

This distinction follows Core directly:

```text
SemanticTopology
       │
       │ persists
       ▼
organizational identity

SemanticTopologyState
       │
       │ changes
       ▼
concepts + semantic relations at a revision
```

A topology evolves by constructing new valid states, not by mutating an existing one.

`TopologyRevision` is a positive monotonically increasing revision number scoped to one topology.

Revision identifies ordering.

It is not the history itself.

History is represented through Events connecting topology states.

---

## Topology evolution

Creation and revision are organizational occurrences.

```python
class SemanticTopologyCreated(Event):
    topology: SemanticTopology
    state: SemanticTopologyState
```

```python
class SemanticTopologyRevised(Event):
    topology: SemanticTopology
    previous: SemanticTopologyState
    current: SemanticTopologyState
```

The initial published state has revision `1`.

For a valid revision event:

```text
previous.topology == current.topology
current.revision  == previous.revision + 1
```

The states remain immutable.

The event records that one published topology state succeeded another.

This gives ST both:

```text
current semantic structure
          +
semantic change history
```

without adding topology history to Core or treating a revision counter as sufficient provenance.

A revision may:

* add a Concept
* stop recognizing a Concept in the published topology
* add or remove a semantic Relation
* replace one semantic Relation with another
* add or remove Context from an assertion
* split a previously unified meaning
* establish equivalence among previously distinct meanings
* withdraw equivalence when meanings diverge
* change a hierarchical relationship
* refine an ambiguous relationship as more evidence becomes available

Concept identity should remain stable when the meaning itself remains stable.

Relationships are allowed to evolve around it.

---

## Semantic relations

Semantic relationships are typed `Relation` refinements whose endpoints are Concepts.

```python
class SemanticRelation(Relation[Concept, Concept]):
    context: Context | None = None
```

The relation class is the kind of semantic assertion.

There is no `relation_type` field.

The initial ST vocabulary is deliberately small.

### Equivalent

Two Concepts express no organizationally relevant semantic distinction within the applicable scope.

```text
Customer ←──── equivalent ────→ Member
```

Properties:

* symmetric
* transitive where the same compatible Context applies
* preserves both Concept identities
* may be revised or withdrawn if organizational meaning changes

`Equivalent` does not mean that the source systems have identical data shapes, identifiers, constraints, implementations, or operational responsibilities.

It asserts semantic equivalence, not implementation equality.

Where equivalence holds only under particular conditions, the relation must carry the applicable `Context`.

---

### Broader

The source Concept semantically subsumes the target Concept.

```text
Transaction ───── broader ─────► Payment
```

Properties:

* directional
* irreflexive
* acyclic within one published topology state
* transitive closure may be derived

The inverse `narrower` view can be derived and does not require a second stored Relation.

`Broader` concerns meaning.

It does not assert inheritance between implementation classes.

---

### Related

Two Concepts have an organizationally meaningful association without asserting equivalence, hierarchy, or overlap.

```text
Customer ←──── related ────→ Household
```

Properties:

* symmetric
* non-transitive

`Related` should be used only when the relationship itself is meaningful. It is not a generic substitute for “we noticed these two things near each other.”

---

### CloseMatch

Two Concepts are sufficiently similar to support discovery, retrieval, candidate mapping, or bounded translation, but they are not safe to treat as equivalent.

```text
Payment ←──── close match ────→ Transaction
```

Properties:

* symmetric
* non-transitive
* weaker than `Equivalent`

`CloseMatch` is useful precisely because semantic alignment is not binary.

---

### Overlap

Two Concepts share part of their meaning while each retains relevant meaning not contained by the other.

```text
Merchant ←──── overlap ────→ Counterparty
```

Properties:

* symmetric
* non-transitive
* neither Concept semantically subsumes the other
* does not imply equivalence

`Overlap` should be used only where the shared and non-shared meaning can be explained well enough for the assertion to be useful.

If that cannot be established, the relationship remains unknown or may remain a candidate outside the published topology.

---

## Context

Semantic relationships are not always universally true.

For example:

```text
Member equivalent Customer
    within RetailBankingContext
```

may be correct while:

```text
Member equivalent Customer
```

without qualification is false or unjustified.

A `Context` on a `SemanticRelation` is therefore part of the semantic assertion itself.

It is not annotation metadata.

```text
Concept A
    │
    ├──── relation ────► Concept B
    │
    └──── applies in ──► Context
```

Absence of Context means the relation is asserted generally within the scope of the published topology.

Context-sensitive reasoning must not combine relations as though their contexts were automatically interchangeable.

---

## Topology invariants

A valid `SemanticTopologyState` must satisfy at least the following invariants:

1. `topology` identifies the persistent `SemanticTopology` whose state is represented.

2. `revision` is positive.

3. Every member of `concepts` is a `Concept`.

4. Every member of `relations` is a `SemanticRelation`.

5. Every semantic relation's source and target are Concepts contained in the same topology state.

6. A semantic relation may not use a non-Concept endpoint.

7. `Broader` may not be reflexive.

8. The directed `Broader` graph must remain acyclic.

9. Symmetric relation classes have symmetric semantics even when only one canonical edge is stored.

10. `Equivalent` never collapses Concept identity.

11. Transitive reasoning may combine assertions only where their Contexts are compatible.

12. Absence of a semantic relation means unknown or undeclared, not false.

13. A candidate relation does not become part of an authoritative topology merely because software or a model proposed it.

14. Publication of a new topology state does not modify or invalidate the originating local semantic models.

15. A `SemanticTopologyRevised` event must connect states belonging to the same topology and advance the revision monotonically.

Validation protects these structural and semantic invariants.

It must not attempt to predefine the organization's Concepts.

---

## Topology facts are not topology management

Semantic Topology represents the organization's accepted structure of meaning.

It does not own the process by which the organization discovers, debates, approves, rejects, or publishes that structure.

These are separate concerns.

A topology-management application might perform:

```text
observe
   ↓
discover or infer candidate relationship
   ↓
construct proposal
   ↓
review / validate / authorize
   ↓
publish revised topology state
```

But that lifecycle is not itself the Semantic Topology.

If an organization needs that process represented explicitly, it can model it using ONTOK Core and, where execution is required, an execution module of its own.

For example:

```text
Role
  + Goal
  + Action
  + Work
  + Event
  + Rule
  + Context
```

can describe who may review semantic changes, toward what end, under what conditions, and what occurred.

ST does not need generic workflow fields to duplicate those semantics.

---

## Emergence

Semantic Topology does not require a top-down enterprise taxonomy.

It should emerge from the organization that already exists.

Candidate Concepts and semantic relationships may be discovered from:

* ONTOK declarations
* application models
* database schemas
* knowledge graphs
* Fabric Ontologies
* Neptune graphs
* APIs
* event contracts
* documents
* policies
* identity models
* external ontologies
* operating language
* acquired systems
* other structured or unstructured sources

Deterministic software should establish relationships where semantics are mechanically known.

Models may assist where interpretation is required.

Examples include:

* identifying candidate Concepts
* interpreting unfamiliar schemas
* proposing possible equivalence
* identifying broader or narrower relationships
* detecting semantic drift
* explaining why two concepts differ
* classifying new organizational language
* identifying possible overlap

The output of inference is a **candidate assertion**, not an authoritative semantic fact.

A model does not gain organizational authority by being confident.

Only an accepted `SemanticRelation` contained in a published `SemanticTopologyState` belongs to the topology.

How acceptance authority is established is an organizational governance concern and may itself be represented using ONTOK.

**Models infer. Software and organizational authority govern.**

---

## Independent ontologies remain independent

Consider two teams that already invested significantly in modeling the same organization.

The first operates an ontology-backed graph in AWS Neptune:

```text
Customer
Account
Transaction
Merchant
```

The second operates a Microsoft Fabric Ontology:

```text
Member
FinancialAccount
Payment
Counterparty
```

Their models may differ in:

* naming
* shape
* cardinality
* granularity
* relationship direction
* lifecycle
* context
* operational purpose

ST does not ask which ontology is the real one.

Adapters or integration code expose their relevant meanings as Concepts.

The organization can then publish assertions such as:

```text
Neptune.Customer
    ── Equivalent ──
Fabric.Member
```

```text
Neptune.Transaction
    ── Broader ──
Fabric.Payment
```

```text
Neptune.Merchant
    ── Overlap ──
Fabric.Counterparty
```

or:

```text
Neptune.Customer
    ── Equivalent ──
Fabric.Member

    within RetailBankingContext
```

Neither source ontology is rewritten.

Neither loses its local identity.

Neither becomes a hidden master schema.

The semantic relationship between them becomes an organizational fact independent of either platform.

That relationship can then be used by software that needs to translate, query, reason, retrieve, synchronize, or operate across those boundaries.

---

## Provenance and source identity

Semantic Topology must preserve Concept identity without embedding source-system provenance as opaque string metadata.

Where provenance matters, source systems, ontology artifacts, schema elements, or other origins should themselves be modeled as appropriate ONTOK Nodes or through source-specific adapter types and related using typed Relations.

ST does not prescribe one universal source model because different source technologies expose different semantic artifacts.

The invariant is simpler:

> A Concept's organizational identity and semantic relationships must not depend on parsing a source-system string convention.

Adapters may supply richer provenance while ST remains concerned with meaning.

---

## Ambiguity, disagreement, and absence

Semantic Topology must not force certainty where the organization does not have it.

The absence of a relation means:

```text
unknown or undeclared
```

not:

```text
false
```

Weak semantic relationships such as `CloseMatch`, `Related`, and `Overlap` allow the organization to represent useful knowledge without pretending that equivalence has been established.

Candidate mappings that remain disputed or insufficiently supported should remain outside the published topology until accepted.

ST does not initially introduce universal `NotEquivalent`, confidence-score, or probabilistic relation primitives.

Domains that require explicit contradiction, confidence, evidence, or adjudication may refine the model in additional modules without weakening the semantics of accepted ST assertions.

---

## Relationship to execution

Semantic Topology owns semantic structure.

It does not own execution mechanics.

An application may use Core to represent topology-management work without creating a separate semantic model for that process.

For example:

```text
SemanticRelationshipProposed
            ↓
        ReviewWork
            ↓
SemanticTopologyRevised
```

The model may have proposed the relationship.

The organizational model determines the Role, Goal, Rule, Context, and meaning involved.

Transport may carry those facts without owning any of those semantics.

ST therefore remains a semantic capability while participating naturally in executable ONTOK applications.

---

## SKOS interoperability

SKOS is a useful interchange vocabulary for Semantic Topology.

It is not ST's programming model.

Natural projections include:

```text
ONTOK Concept       ↔ skos:Concept

SemanticTopology    ↔ skos:ConceptScheme

Broader             ↔ skos:broader

Related             ↔ skos:related

Equivalent          ↔ skos:exactMatch

CloseMatch          ↔ skos:closeMatch
```

`Overlap` has no assumed lossless SKOS equivalent and may remain an ONTOK-specific semantic Relation.

Context-qualified semantic assertions may also require RDF, OWL, SHACL, named graphs, reification, or another representation capable of preserving their conditions.

A projection must not silently discard semantics merely to fit a target vocabulary.

Where a lossless representation is unavailable, the adapter should preserve the additional semantics explicitly or report that the projection would be lossy.

Python users should not need to program against SKOS classes to use ST.

SKOS is an interoperability surface.

ONTOK ST is the organizational capability.

---

## Python surface

The developer experience should remain small and ordinary.

Conceptually:

```python
from ontok.core import Concept, Context
from ontok.st import (
    Broader,
    CloseMatch,
    Equivalent,
    Overlap,
    Related,
    SemanticTopology,
    SemanticTopologyCreated,
    SemanticTopologyRevised,
    SemanticTopologyState,
    TopologyRevision,
)
```

An application should be able to:

* construct Concepts
* construct semantic Relations
* construct and validate a topology state
* publish an initial topology
* revise it immutably
* inspect its semantic structure
* query or traverse its relationships
* serialize it
* project it through adapters
* use it as ordinary program data

No generic `kind`, `type`, or relation discriminator fields should be introduced to simulate subclassing.

The class remains the kind.

---

## Specification placement

Semantic Topology is the `st` module.

It imports ONTOK Core and does not enlarge the thirteen-primitive kernel.

The implementation-independent specification is:

```text
spec/ontok-st.xml
```

It defines the semantic contracts for:

```text
SemanticTopology
SemanticTopologyState
TopologyRevision

SemanticRelation
Equivalent
Broader
Related
CloseMatch
Overlap

SemanticTopologyCreated
SemanticTopologyRevised
```

along with their invariants and interoperability expectations.

The Python realization is:

```text
ontok.st
```

and depends one-way on:

```text
ontok.core
```

Other modules may depend on ST.

ST must not require them in order to define its own semantics.

---

## Proof obligation

Semantic Topology is not complete because its classes can be instantiated.

It must survive contact with independently developed semantic systems in the same way that an execution extension must survive contact with real execution structure.

The proving scenario is:

1. Begin with two independently designed ontologies representing overlapping parts of the same organization.

2. Preserve both models unchanged.

3. Expose their relevant meanings as distinct Concepts.

4. Represent exact equivalence where justified.

5. Represent hierarchy, weak similarity, association, and overlap where equivalence is not justified.

6. Represent at least one relationship that is valid only within a Context.

7. Validate all topology invariants.

8. Publish an initial immutable topology state.

9. Revise at least one semantic relationship without mutating previous states.

10. Preserve the revision history through topology Events.

11. Demonstrate that a model-generated candidate relationship does not become authoritative merely by being proposed.

12. Project supported semantics into SKOS-compatible RDF without silently losing unsupported ONTOK semantics.

13. Use the resulting topology as ordinary typed application data.

If satisfying this scenario requires source systems to adopt the same schema, collapse Concept identities, add generic runtime type tags, place workflow state inside ST, or delegate semantic authority to an LLM, the design has failed.

---

## What Semantic Topology is not

Semantic Topology is not:

* a Core primitive
* a universal taxonomy
* a canonical enterprise schema
* a master-data-management system
* a requirement that source systems share identifiers
* a requirement that equivalent Concepts become one Concept
* a replacement for domain ontologies
* a replacement for Fabric Ontology, Neptune, or other semantic systems
* an LLM-owned knowledge structure
* a workflow engine
* a generic proposal-management system
* a requirement that source systems adopt ONTOK internally
* a graph container whose edges merely carry semantic labels

It is the organization's evolving, explicit structure of relationships among independently developed meanings.

---

## Completion criterion

Semantic Topology is complete when ONTOK can take independently developed semantic models of the same organization, preserve those models as legitimate local representations, express the relationships among their meanings as validated typed facts, qualify those assertions by organizational Context where necessary, publish and revise the topology immutably while preserving its history, distinguish accepted semantic structure from inferred candidates, expose the result as ordinary application data, and project its semantics into external representations without silently weakening them.

At that point ONTOK can represent not only what an organization declares and means, but how the different ways the organization understands itself fit together.
