# ONTOK

## Write the organization as software.

ONTOK is a modular declarative semantic language for expressing the kinds an organization contains, constructing facts that satisfy those kinds, and carrying shared meaning across software that will never share one schema.

An organization already has customers, invoices, employees, roles, approvals, states, events, goals, policies, relationships, and concepts. Software usually represents fragments of that reality in local schemas and application models. ONTOK provides a small semantic kernel from which those organizational kinds can be declared directly in software.

```python
class Invoice(Entity):
    ...

class HireApproved(Event):
    ...

class ReportsTo(Relation):
    ...

class HiringManager(Role):
    ...
```

You do not call ONTOK as a service. You import the kernel and grow an ontology.

A CRM row, SCIM resource, ticket, graph record, API payload, document interpretation, or agent proposal can then become an instance of a declared organizational kind. The declaration constructs successfully or it does not. Meaning that matters to the program no longer has to be reconstructed from field names, prompts, integration code, and documentation at every boundary.

ONTOK does not require the organization to become one application, one graph, or one schema. It gives independently evolving systems a common semantic grammar.

---

## The kernel

ONTOK Core contains twelve primitives:

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

Meaning
  Concept
  Context

Governance
  Rule
```

The progression matters: **structure → reality → agency → meaning → governance**.

`Node` and `Connection` establish the graph. `Entity`, `Relation`, `State`, and `Event` let the organization represent what persists, how things associate, where they stand, and what occurs. `Role`, `Goal`, and `Action` make intentional organizational behavior explicit. `Concept` and `Context` represent meaning and the conditions under which meaning or action applies. `Rule` governs action within that same model.

Twelve primitives are enough to provide the grammar. They are not an enterprise data model. A bank, manufacturer, hospital, retailer, or software company should not get its domain ontology from ONTOK Core.

It should write its own.

### The class is the kind

ONTOK expresses domain kinds through refinement.

```python
class Customer(Entity):
    ...

class PaymentReceived(Event):
    ...

class Owns(Relation):
    ...

class AccountOwner(Role):
    ...
```

`Customer(Entity)` is the kind. `PaymentReceived(Event)` is the kind. `Owns(Relation)` is the kind.

Instances carry organizational facts. Classes carry organizational kinds.

That distinction keeps the kernel small while allowing the organizational model to become arbitrarily specific. Modules refine the kernel in the same way, and organizations can build their own semantic packages without pushing every useful concept back into Core.

---

## Construct organizational facts

The important thing about ONTOK is not that it uses Python classes. It is that organizational facts can retain their meaning as they move through software.

A pipeline can construct a `Customer`. An identity feed can construct an organizational person and membership. A workflow can construct a `HireApproved` Event. Software claiming that an organizational Action occurred can represent the Entity that acted, the Role through which it acted, the Goal toward which it acted, and the Event memorializing what occurred.

Those values can then cross application boundaries without being reduced to records whose interpretation must be independently rediscovered by every consumer.

A graph can persist them. A queue can move them. A workflow can carry them. An agent can propose them. A Rule can constrain them. Another system can receive them.

The execution technology can change without changing the semantic grammar.

---

## Meaning is bigger than type

A local type tells a program what kind of thing it has declared. It does not tell the organization how that declaration relates to meanings defined somewhere else.

A CRM may have `Customer`. A servicing platform may have `Member`. A database column named `cust_no` may encode the customer concept without saying so explicitly anywhere in the system.

`Concept` exists for meaning and alignment.

```text
cust_no  ──means────────→  Customer

Member   ──corresponds──→  Customer
```

This separation matters because local models are allowed to remain local. ONTOK does not need to rename every declaration or force every system onto the same class hierarchy before the organization can understand them together.

But once an organization has many Concepts, another problem appears. It has explicit meanings without an explicit structure among those meanings.

That is what ONTOK Semantic Topology adds.

---

## ONTOK ST: Semantic Topology

**ONTOK ST is the evolving structure of meaning across the organization.**

Concept gives a declaration meaning. ONTOK ST lets independently developed meanings form an organizational structure.

Consider one business with an application graph in AWS Neptune and another domain modeled independently in Microsoft Fabric:

```text
AWS Neptune                 Microsoft Fabric

Customer                    Member
Account                     FinancialAccount
Transaction                 Payment
Merchant                    Counterparty
```

Neither model needs to become canonical. Both may be correct for the work they perform.

ONTOK ST can make their semantic relationships explicit:

```text
Customer          Equivalent     Member
FinancialAccount  Broader        Account
Transaction       CloseMatch     Payment
Merchant          Overlap        Counterparty
```

Those relationships now belong to the organization rather than to Neptune, Fabric, an integration mapping, or the memory of the people who built them.

ONTOK ST is not a universal taxonomy. Every organization develops its own topology because every organization develops its own meanings and distinctions. It is also not a thirteenth primitive; it is a module constructed from the semantic grammar ONTOK already provides, principally Concepts, Relations, and Context.

The topology can emerge from the organization that already exists: classes, schemas, graphs, APIs, events, documents, policies, code, external ontologies, and operating language can all reveal semantic structure.

It also evolves. New systems introduce new Concepts. Definitions drift. Concepts split or merge. Acquisitions introduce parallel vocabularies. A relationship once treated as equivalent may become only a close match, or may apply only within a particular Context.

That evolution can be observed and governed:

```text
observe
  → discover or infer
  → propose
  → validate
  → accept, reject, or revise
  → continue observing
```

Deterministic software can establish relationships where semantics are known mechanically. Models can help interpret ambiguous schemas, documents, code, policies, and graph neighborhoods. ONTOK gives the resulting proposals a common form that software can validate, persist, reject, revise, and govern.

SKOS is a natural interoperability model for ONTOK ST because it already provides standardized representations for Concepts, concept schemes, broader and narrower relationships, related concepts, and semantic mappings such as exact and close matches. SKOS is an interchange vocabulary; ONTOK ST is the organizational capability.

---

## Many runtimes, one semantic layer

ONTOK does not need to own execution.

Temporal can orchestrate a workflow. Pydantic Graph can run a graph. NATS can move messages. Neptune can persist a graph. Fabric can expose an ontology. PostgreSQL can hold application state. An LLM can infer.

ONTOK defines what the organizational values moving through those systems mean.

That distinction becomes especially important in agentic systems. A typed agent can receive an `Invoice`, propose a `HireApproved`, act through a `Role`, pursue a `Goal`, or return an Event. A graph runner or workflow engine can move those values through a deterministic control structure without inventing a parallel semantic model.

Pydantic's agents and graphs describe how a run proceeds. **ONTOK describes what the run is allowed to be.**

A vast agent architecture without shared semantics is still a collection of systems inventing meaning at its boundaries. ONTOK gives those systems one organizational grammar without requiring them to share one runtime.

Language models fit naturally into that architecture, but they do not own it. Models can discover Concepts, propose alignments, classify declarations, explain semantic differences, and detect candidate drift. Software owns control flow, validation, durable state, authority, and execution.

Models infer. Software governs.

---

## Core stays small. Modules refine it.

ONTOK grows through modules rather than kernel inflation.

The project currently includes:

```text
ontok-core
ontok-vsm
ontok-scim
ontok-st
```

`ontok-core` provides the twelve-primitive kernel.

`ontok-vsm` expresses Value Stream Mapping through ONTOK so performed work and value-stream structure can participate in the same organizational graph as the rest of the business.

`ontok-scim` aligns SCIM identity and organizational structures with ONTOK so standardized identity resources can participate in broader organizational semantics.

`ontok-st` provides Semantic Topology: the evolving structure of meaning among independently declared Concepts, with SKOS as an interchange vocabulary.

A value stream is useful, but it is not a universal primitive. SCIM semantics are useful, but they do not belong in the kernel. Modules let ONTOK become richer while preserving a small universal Core.

Organizations can refine the same kernel into their own packages.

---

## Specification and realization

ONTOK is not defined by its Python implementation.

Each module has an implementation-independent specification that defines its semantics, constraints, refinements, and dependencies. Language implementations realize that semantic contract using the native type systems and tooling of their ecosystems.

```text
ONTOK specification
        ↓
semantic contract
        ↓
language realization
        ↓
executable organizational model
```

The current specifications are expressed in XML. The Python realization uses strict Pydantic models so ONTOK declarations can be constructed and validated directly inside ordinary software.

The specification says what ONTOK means. The realization makes those semantics executable.

Python is the first realization, not the definition of the language.

ONTOK can also project into established standards where they provide useful interoperability. RDF, OWL, and SHACL can represent and validate semantic graphs; SKOS aligns naturally with ONTOK ST; SCIM underpins the identity semantics of `ontok-scim`. Developers can use ONTOK as ordinary typed software without making those standards the programming surface of every application.

---

## Repository

This repository is the canonical home of ONTOK. It contains the implementation-independent specifications, project documentation, language realizations, modules, examples, and tests.

Language realizations live beneath:

```text
packages/<language>/
```

The Python realization is a `uv` workspace under:

```text
packages/python/
├── ontok-core/    → ontok.core
├── ontok-vsm/     → ontok.vsm
├── ontok-scim/    → ontok.scim
└── ontok-st/      → ontok.st
```

The root documentation describes ONTOK as a language and product. Module and package documentation cover their specific semantics and implementation surfaces.

---

## The Automated Organization

Organizations have always had entities, states, events, relationships, roles, goals, actions, concepts, contexts, and rules. What they have rarely had is one explicit semantic system through which those structures can remain coherent across the software that implements them.

People supplied that missing layer.

They knew that `Member` in one system meant roughly the same thing as `Customer` somewhere else. They knew why a policy applied in one situation and not another. They translated between applications, reports, documents, departments, and operating language. They reconciled contradictions and carried context that software never represented.

Humans were the semantic middleware.

As more of the organization becomes executable through applications, workflows, graphs, agents, and models, that implicit semantic layer becomes part of the runtime architecture. Software cannot reliably operate the organization if every system must independently reconstruct what the organization means.

ONTOK makes that meaning part of the program.

**Write the organization as software. Let its systems share meaning without requiring them to share an implementation.**

---

## License

ONTOK is licensed under the [Apache License 2.0](LICENSE).
