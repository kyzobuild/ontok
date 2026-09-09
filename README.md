# ONTOK

**Make organizational meaning explicit, portable, and executable.**

ONTOK is a modular declarative semantic language for representing an organization as a machine-operable graph and carrying meaning across the independently evolving systems that implement it. Its twelve-primitive Core provides a small grammar for organizational structure, reality, agency, meaning, and governance. Semantic Topology organizes the meanings that emerge across those declarations, while optional modules add reusable organizational capabilities without enlarging the kernel.

ONTOK is designed for organizations in which applications, data platforms, knowledge graphs, policies, people, and intelligent systems all participate in representing and operating the same business. Those systems do not need to share one schema, database, programming language, graph technology, or vendor. They need a durable way to share meaning.

## Why ONTOK Exists

Every significant system contains a partial model of the organization it serves. A CRM defines customers and accounts. An ERP defines products, transactions, and obligations. A data platform introduces analytical entities and measures. A knowledge graph creates another representation. Policies establish concepts and constraints in prose. Application code embeds distinctions that may exist nowhere else. Agents increasingly construct additional working models from schemas, retrieved documents, tool descriptions, and the context available during execution.

Different representations are not necessarily defects. They usually exist for different purposes. A customer-facing application may legitimately use a narrower idea of `Customer` than a financial platform. A graph designed for fraud analysis may organize transactions differently from a servicing ontology. The architectural problem is that most organizations have no durable semantic layer capable of expressing what these representations mean, how they correspond, where they differ, and which meanings should survive the systems that currently implement them.

Traditional enterprise modeling has often tried to solve this by defining a canonical model and asking every system to conform to it. ONTOK separates semantic coherence from implementation convergence. Local models remain legitimate while the organization gains a common language for describing and relating them.

That becomes increasingly important as software assumes more operational responsibility. Semantic inconsistency is inconvenient when systems merely record work. It becomes part of execution when applications, agents, and automated processes interpret concepts such as approval, entitlement, risk, obligation, customer, employee, product, incident, or authority.

## One Organization, Many Models

Consider a business with one major application architecture represented in AWS Neptune and another modeled independently in Microsoft Fabric.

```text
AWS Neptune                 Microsoft Fabric

Customer                    Member
Account                     FinancialAccount
Transaction                 Payment
Merchant                    Counterparty
```

Both models may be internally correct, and neither needs to be treated as the canonical representation of the business. The useful question is how their meanings correspond.

ONTOK can represent that `Customer` and `Member` are equivalent in the relevant organizational context, that `FinancialAccount` is broader than `Account`, that `Transaction` is only a close match for `Payment`, or that `Merchant` overlaps with `Counterparty` without being interchangeable with it.

The source systems remain independent. The semantic relationships become explicit organizational structure rather than knowledge hidden in integration code, architecture diagrams, or individual people's heads.

## ONTOK Core

ONTOK Core is a deliberately small kernel of twelve primitives.

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

The kernel does not attempt to enumerate the kinds of customers, invoices, products, people, systems, policies, resources, or workflows an organization might contain. Those domain kinds are created by refining the kernel.

`Node` and `Connection` establish the graph. `Entity`, `Relation`, `State`, and `Event` describe organizational reality: what persists, how things associate, where they stand, and what occurs. `Role`, `Goal`, and `Action` represent intentional organizational agency. `Concept` and `Context` make meaning and applicability explicit. `Rule` governs action within that same organizational model.

Supporting types provide mechanics such as identity, temporal extent, state standings, schema succession, and memorialization. They support the twelve primitives without expanding the kernel.

## Refinement: From Kernel to Organization

The Core primitives are sortals. Domain semantics are expressed by refining them through ordinary classes rather than attaching instance-level type identifiers.

An organization might define:

```python
from ontok.core import Entity, Event, Relation

class Invoice(Entity):
    pass

class HireApproved(Event):
    pass

class ReportsTo(Relation):
    pass
```

Modules use the same mechanism. ONTOK VSM and ONTOK SCIM can define richer organizational kinds from the same Core without adding new universal primitives merely because a particular domain needs them.

This keeps the kernel small while allowing the language to become specific wherever the organization requires specificity. The class is the kind; the graph contains instances of those refined organizational kinds.

## Meaning and Alignment

Structural precision does not guarantee shared meaning. Two classes can be rigorously defined and still represent overlapping, conflicting, or differently scoped organizational ideas.

`Concept` provides the semantic layer through which declarations acquire meaning and can be aligned. It allows the organization to express relationships such as a field called `cust_no` meaning `Customer`, or a `Member` concept in one system corresponding to a `Customer` concept elsewhere.

This does not require local declarations to be renamed or collapsed. ONTOK preserves the distinction between the declaration and the meaning assigned to it.

Once an organization contains many Concepts, however, another problem appears. Individual meanings exist, but the larger structure among them is still implicit.

Semantic Topology addresses that problem.

## Semantic Topology

Semantic Topology is the evolving organization of meaning across the organizational graph.

A topology contains Concepts and explicit semantic Relations among them. ONTOK initially distinguishes relationships such as equivalence, broader meaning, association, close matching, and overlap. A relationship may also be conditional on Context when two meanings correspond only under particular organizational conditions.

Returning to the Neptune and Fabric example, an organization's topology might contain:

```text
Customer         Equivalent     Member
FinancialAccount Broader        Account
Transaction      CloseMatch     Payment
Merchant         Overlap        Counterparty
```

The topology is not a taxonomy supplied by ONTOK and is not another canonical enterprise schema. It belongs to the organization and develops from the meanings that actually appear in its systems and operations.

A Semantic Topology also evolves. New systems introduce new Concepts, operating distinctions change, formerly equivalent meanings diverge, acquisitions bring parallel vocabularies, and the organization may discover structure that previously existed only implicitly. ONTOK represents that evolution through successive validated revisions while preserving Concept identity wherever the underlying meaning remains stable.

Semantic Topology completes the meaning layer of ONTOK because it allows the organization to represent not only individual meanings, but also the shape formed among those meanings across independently evolving systems.

## An Emergent Semantic Model

A useful organizational semantic model does not need to begin with a multi-year effort to define the entire enterprise from the top down. Semantic Topology can develop incrementally from the organization that already exists.

Candidate Concepts and relationships may be discovered from application classes, schemas, APIs, graphs, event contracts, documents, policies, code, external ontologies, and operating language. Some relationships can be established deterministically. Others require semantic judgment.

Language models are useful here because they can interpret names, documentation, examples, relationships, and surrounding context to propose that two Concepts correspond, that one is broader than another, or that a previously valid alignment appears to have drifted. ONTOK gives those proposals a durable representation that software can validate and govern.

The result is an organizational semantic model that can be observed, declared, tested, corrected, and evolved as part of normal operation rather than treated as a static artifact produced once by an architecture program.

## What This Architecture Makes Possible

### Semantic interoperability

ONTOK allows systems to share meaning without requiring them to share physical storage or identical schemas. Neptune, Fabric, relational systems, event streams, application APIs, RDF graphs, documents, and other representations can remain locally appropriate while participating in the same organizational semantics.

This goes beyond serialization compatibility. Two systems may already be able to exchange JSON while disagreeing completely about what the values mean. ONTOK operates at the semantic layer above that exchange.

### Semantic continuity

Applications are often shorter-lived than the meanings they implement. Concepts such as `Customer`, `Approval`, `Product`, `Obligation`, or `Risk` should not have to be reinvented every time the organization changes platforms.

By separating organizational meaning from local implementation, ONTOK allows system replacement, re-platforming, restructuring, and acquisition to occur while preserving an explicit account of the semantics that need to survive the change.

### Semantic observability

Organizations monitor infrastructure, application behavior, and data quality, but semantic health is usually visible only through downstream symptoms. Once Concepts and alignments become explicit, software can identify duplicate meanings, unresolved mappings, competing definitions, broken equivalences, hierarchy problems, and concepts whose implementations have drifted apart.

Schema drift identifies structural change. Semantic drift identifies a change in what the organization means.

### Portable automation

Queries, policies, applications, and agents can increasingly depend on organizational meaning rather than only on the names and structures exposed by a particular system.

A request such as "show customers whose payment behavior changed after entering delinquency" contains organizational concepts that may be realized across several platforms. ONTOK can provide the semantic layer through which a query planner, application, or agent determines what those concepts correspond to in each system.

A business rule can similarly be expressed in terms of organizational Entities, States, Roles, Actions, Concepts, and Contexts while integrations determine how that rule is enforced by the current application landscape.

ONTOK is not itself a graph database, query engine, workflow system, or agent framework. It provides semantic structure those systems can share.

## Models Infer, Software Governs

ONTOK assumes language models will increasingly participate in ordinary software. Semantic interpretation is one of their useful roles because many mappings cannot be derived from structure alone. A model can inspect schemas, documentation, examples, policy, surrounding relationships, and actual usage to propose semantic structure.

That inference does not make the model the authority over the organizational graph. Software can decide when inference is requested, what evidence is available, which validations apply, who or what may accept a change, and how an approved declaration becomes part of the topology.

```text
observe systems and graph
          ↓
request bounded inference
          ↓
construct proposed ONTOK declaration
          ↓
validate semantics and authority
          ↓
accept, reject, or revise
          ↓
publish the next topology revision
```

This preserves a useful division of responsibility. Models contribute bounded inference and judgment where ambiguity exists; software owns control flow, durable state, validation, authorization, and execution.

The same ONTOK structures remain usable in systems that contain no language model at all.

## Modular by Design

ONTOK Core defines the universal organizational grammar. Additional capabilities are developed as modules with explicit one-way dependencies rather than being pushed into the kernel.

The project currently includes:

* `ontok-core`, the universal semantic foundation.
* `ontok-vsm`, Value Stream Mapping semantics built from Core.
* `ontok-scim`, SCIM-aligned identity and organizational semantics built from Core.

A value stream is an important organizational structure, but it is not a universal primitive. SCIM provides useful standardized identity semantics, but those semantics do not belong inside the kernel. Modules allow ONTOK to become richer without confusing domain utility with ontological necessity.

Organizations can use the same refinement mechanism to create their own semantic packages.

## Specification and Realization

ONTOK is defined independently of any single programming language.

Each module has an implementation-independent specification describing its constructs, refinements, constraints, and dependencies. Language implementations realize those semantics through the native type systems and tooling of their ecosystems.

The Python implementation is therefore an executable realization of ONTOK rather than the definition of ONTOK itself.

```text
ONTOK specification
        ↓
semantic contract
        ↓
language realization
        ↓
executable declarations
```

The current specifications are expressed in XML. The Python realization implements them as strict Pydantic classes and validators. The specification and implementation evolve together so that the language remains both implementation-independent and directly usable inside real programs.

## Standards and Interoperability

ONTOK does not need to replace standards that already provide useful semantic infrastructure. RDF, OWL, SHACL, SKOS, SCIM, and related standards can be used where they improve interchange, validation, or integration.

Semantic Topology, for example, maps naturally to SKOS concepts, concept schemes, and semantic relationships. ONTOK SCIM can connect standardized identity resources to the larger organizational graph. RDF, OWL, and SHACL can provide external semantic representations where those ecosystems are appropriate.

These standards are interoperability surfaces rather than the required application programming model. A developer should be able to use ONTOK as ordinary typed software without first becoming a specialist in the Semantic Web stack.

## Using ONTOK

The Python realization is designed to make ONTOK ordinary program structure.

```python
from ontok.core import Entity, Relation

class Customer(Entity):
    pass

class Account(Entity):
    pass

class Owns(Relation):
    source: Customer
    target: Account
```

The value is not the amount of code required to declare `Customer`. The value is that the declaration has a defined semantic role within a larger organizational graph and can participate in validation, graph projection, Semantic Topology, query planning, governance, standards interchange, and intelligent software.

Pipelines, services, applications, graph adapters, query systems, and agent harnesses can consume and emit the same ONTOK structures directly.

## Repository Structure

This repository is the canonical home of ONTOK. It contains the implementation-independent specifications, core documentation, language realizations, extension modules, examples, and tests.

Language realizations live under:

```text
packages/<language>/
```

so each language can use its native workspace, package management, validation, and publishing conventions while implementing the same ONTOK specifications.

The Python realization lives under `packages/python/` as a `uv` workspace of independently publishable packages sharing the `ontok` namespace:

```text
packages/python/
├── ontok-core/    → ontok.core
├── ontok-vsm/     → ontok.vsm
└── ontok-scim/    → ontok.scim
```

`ontok-vsm` and `ontok-scim` depend on `ontok-core`. Future modules should preserve the same explicit dependency direction so optional semantics do not leak backward into the universal kernel.

The root documentation describes ONTOK as a language and product. Module and package documentation can go deeper into their specific semantics, APIs, and implementation details.

## ONTOK and the Automated Organization

ONTOK is built around a broader premise: organizations are becoming increasingly executable.

An organization already has entities, states, events, relationships, roles, goals, actions, concepts, contexts, and rules whether its software represents those things explicitly or not. Historically, much of the semantic continuity among them has been supplied by people. Humans knew that different systems used different words for roughly the same thing, understood when a policy exception applied, reconciled inconsistent representations, translated between organizational vocabularies, and carried context that software never modeled.

As more operational responsibility moves into applications, agents, models, automated workflows, and other software, that implicit semantic layer becomes part of the runtime problem. An organization cannot reliably automate structures it cannot describe, and it cannot distribute that automation across independently evolving systems if each system has to reconstruct organizational meaning independently.

ONTOK provides a portable semantic substrate for that environment. It does not require the organization to become one application, one database, one graph, or one ontology. It allows independently evolving systems to remain locally appropriate while participating in a coherent, machine-operable understanding of the same organization.

The systems do not need to share an implementation. They need a way to share meaning.
