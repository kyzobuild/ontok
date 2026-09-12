# ONTOK

## Write the organization as software.

Large organizations model the same business concepts over and over: in applications, APIs, event contracts, data platforms, graphs, policies, workflows, and AI systems.

Those models are rarely identical. One system has a `Customer`; another has a `Member`. One graph models a `Payment`; another models a broader `Transaction`. The differences may be legitimate, but the relationships among them usually live in integration code, documentation, prompts, and people's heads.

That works until more software needs to understand and act on the business directly.

**ONTOK is a small semantic language for making organizational meaning explicit in software without requiring every system to share one schema, graph, platform, or runtime.**

Organizations refine its kernel into their own kinds. Programs construct facts that satisfy those kinds. Extensions can then operate over the same organizational meaning rather than inventing another model of it.

You do not call ONTOK as a service.

You import the language and refine it into the organization you actually have.

---

## The types do organizational work

ONTOK Core is deliberately small. Its primitives distinguish things software routinely collapses together.

An `Entity` persists. A `State` is a condition that goes on an Entity. An `Event` occurs.

Organizational agency has structure too:

```python
class Action(Node):
    role: Role
    goal: Goal


class Work(Entity):
    action: Action
```

An `Action` is a declared doing: through this organizational capacity, toward this intended end.

`Work` is the persistent undertaking of that declaration.

Governance composes from the same model:

```python
class Rule(Node):
    context: Context
    doing: Action
```

A `Context` is a situation constituted by States. A `Rule` constrains declared Action within that situation.

These are application components, not labels attached to application data.

A domain refines them into the kinds it actually needs:

```python
class Customer(Entity): ...


class StrategicAccount(State):
    customer: Customer


class AccountManager(Role): ...


class AccountReviewed(Goal): ...


class ReviewAccount(Action): ...
```

**The class is the kind. The value is the fact.**

The Python realization uses strict, immutable Pydantic models, so those facts participate in ordinary program construction and validation rather than living in a separate semantic store.

The complete Core is still only:

```text
Structure    Node · Connection
Reality      Entity · Relation · State · Event
Agency       Role · Goal · Action · Work
Meaning      Concept · Context
Governance   Rule
```

This is not an enterprise data model.

A bank, manufacturer, hospital, retailer, or software company should define its own domain ontology by refining this grammar.

---

## Local models can stay local

Now consider a normal brownfield enterprise.

One team has already invested heavily in an ontology-backed graph in AWS Neptune. Another has independently built a Microsoft Fabric Ontology for the same company.

Both contain real business knowledge:

```text
AWS Neptune                 Microsoft Fabric

Customer                    Member
Account                     FinancialAccount
Transaction                 Payment
Merchant                    Counterparty
```

Their names differ. Their shapes differ. Their cardinalities, granularity, lifecycle assumptions, and relationships may differ.

Neither model needs to be wrong.

And neither needs to become the canonical replacement for the other.

ONTOK Semantic Topology is designed to represent the organizational relationships among those independently developed meanings:

```text
Neptune.Customer
       │
       └──── equivalent / close ──── Fabric.Member


Neptune.Transaction
       │
       └──── broader ─────────────── Fabric.Payment


Neptune.Merchant
       │
       └──── overlap ─────────────── Fabric.Counterparty
```

A relationship may also be true only within a particular `Context`.

The local ontologies remain local. Their identities and useful distinctions survive.

What becomes explicit is **how the organization understands their relationship**.

That semantic topology can evolve as systems change, concepts split or converge, acquisitions introduce new vocabularies, and previously assumed equivalences stop being true.

ONTOK does not solve semantic disagreement by forcing convergence.

It makes the disagreement, correspondence, and context representable.

---

## One kernel, different capabilities

ONTOK grows through modules rather than by turning Core into a universal model.

```text
                         Core
                          │
            ┌─────────────┼─────────────┐
            ▼             ▼             ▼
           ST             VSM           SCIM
       semantic         value         identity
       topology         streams
```

`ontok-st` develops the evolving relationships among independently defined Concepts.

`ontok-vsm` represents value-stream structure and performed work.

`ontok-scim` aligns standardized identity structures with the broader organizational model.

Organizations can build their own modules the same way.

A capability becomes part of ONTOK by composing the semantic kernel, not by adding every useful business concept to it.

---

## Why this matters for AI

Most organizations have always depended on an implicit semantic layer.

People know that `Member` in one system is roughly `Customer` somewhere else. They know which definition of `Account` applies in a particular conversation. They know why a policy applies in one situation and not another.

People have been the semantic middleware.

As applications, agents, and models perform more organizational work directly, that implicit layer becomes a runtime dependency. A model cannot reliably inherit years of organizational context simply because the relevant systems are connected to it.

ONTOK makes the meaning software-addressable.

Models can interpret, classify, discover candidate relationships, and reason over organizational facts.

They do not need to become the authority that defines those facts or owns the program's control flow.

---

## Specification and realization

ONTOK is not defined by Python.

Its modules have implementation-independent specifications describing their semantics, refinements, constraints, and dependencies.

```text
ONTOK specification
        │
        ▼
 semantic contract
        │
        ▼
language realization
        │
        ▼
 ordinary software
```

The current specifications are expressed in XML.

Python is the first realization, using Pydantic to make ONTOK kinds and facts ordinary typed program values.

External standards and platforms can participate where useful. RDF, OWL, SHACL, SKOS, SCIM, graph databases, Fabric Ontology, and other representations can exchange or project ONTOK semantics without becoming ONTOK's programming model.

**The specification defines the language. A realization makes it usable.**

---

## Explore the project

The repository contains the implementation-independent specifications, Python realization, modules, examples, tests, and design documentation.

The Python workspace lives under:

```text
packages/python/
```

The shortest paths into the architecture are:

```text
ontok-core    the semantic kernel
ontok-st      semantic topology
ontok-vsm     value streams
ontok-scim    identity
```

Start with Core if you want to understand the language.

Look at ST if your organization already has multiple schemas, graphs, ontologies, or vocabularies describing overlapping business reality.

ONTOK does not require those systems to become one system.

It gives them a language in which their meaning can become explicit, related, validated, and operated on as software.

**Write the organization as software.**

## License

ONTOK is licensed under the [Apache License 2.0](LICENSE).
