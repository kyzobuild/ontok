# ONTOK

## Write the organization as software.

Large organizations model the same business concepts repeatedly: in applications, APIs, event contracts, data platforms, graphs, policies, workflows, and AI systems.

Those models are rarely identical. One system has a `Customer`; another has a `Member`. One graph models a `Payment`; another models a broader `Transaction`. Each may be correct for the work it performs, but the relationships among them are usually reconstructed in integration code, documentation, prompts, and people's heads.

**ONTOK makes organizational meaning explicit in software without requiring every system to share one schema, graph, platform, or runtime.**

You define the kinds your organization contains, construct facts that satisfy those kinds, and make the relationships among independently developed meanings explicit.

```python
class Customer(Entity): ...


class PaymentReceived(Event): ...


class AccountOwner(Role): ...
```

You do not call ONTOK as a service.

You import the language and refine it into the organization you actually have.

---

## What this looks like

ONTOK starts with a small semantic kernel.

Organizations refine that kernel into their own domain:

```python
class HiringManager(Role): ...


class PositionFilled(Goal): ...


class ApproveHire(Action): ...
```

Classes declare organizational **kinds**.

Instances are organizational **facts**.

A CRM record, graph node, API payload, event, document interpretation, or agent proposal can be constructed as one of those facts. If the declaration has constraints, the value satisfies them or construction fails.

The semantics are therefore not metadata sitting beside the program. They are values the program can actually use.

---

## A small semantic kernel

ONTOK separates concepts that business software often collapses together.

An `Entity` is something whose identity persists.

A `State` is a condition that goes on an Entity.

An `Event` is something that occurs.

```text
Entity ── persists
  │
  └── State ── condition

Event ── occurs
```

Organizational agency is explicit too.

A `Role` is the organizational capacity through which action is taken. A `Goal` is the intended end. An `Action` declares work. `Work` is the persistent undertaking of that declaration.

```text
Role ─┐
      ├──► Action ───► Work
Goal ─┘
      declaration    undertaking
```

`Concept` represents meaning. `Context` represents a situation constituted by states. `Rule` constrains declared action within a context.

The full Core remains small:

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

These are not an enterprise data model.

A bank, manufacturer, hospital, retailer, or software company should define its own `Customer`, `Account`, `Approval`, `Shipment`, `Policy`, and thousands of other organizational kinds by refining this grammar.

---

## Local models can stay local

Consider an organization where one team has already built a substantial ontology in AWS Neptune and another has independently modeled the same business in Microsoft Fabric.

They may contain concepts like:

```text
AWS Neptune                 Microsoft Fabric

Customer                    Member
Account                     FinancialAccount
Transaction                 Payment
Merchant                    Counterparty
```

The shapes will differ.

The names will differ.

The teams may have made different decisions about cardinality, lifecycle, granularity, relationships, and context.

Neither ontology needs to be wrong.

And neither needs to become the canonical replacement for the other.

ONTOK Semantic Topology can make the relationships among those meanings explicit:

```text
Customer          ── equivalent / close ── Member

Transaction       ── broader ───────────── Payment

Merchant          ── overlaps ──────────── Counterparty
```

Those relationships can themselves become organizational facts.

The Neptune model remains useful in Neptune. The Fabric ontology remains useful in Fabric. ONTOK gives the organization a place to express how they relate.

This extends beyond graphs. Application schemas, APIs, event contracts, identity systems, documents, external vocabularies, and AI-generated interpretations can participate in the same semantic topology.

The goal is not one universal schema.

It is shared meaning across systems that are allowed to remain different.

---

## Meaning can participate in execution

Once organizational semantics are ordinary program values, execution does not need to invent a parallel model of the business.

`ontok-ex` demonstrates this directly.

An `Activation` is an occurrence in which declared `Work` becomes enabled.

A `Completion` is an occurrence in which activated Work completes.

Concrete execution types declare the exact Work and exact prerequisite that make an activation valid:

```python
class LeftActivation(Activation):
    work: LeftWork
    prerequisite: BeginningCompletion
```

Multiple prerequisites are represented as a complete typed product:

```python
class BranchesCompleted(BaseModel):
    left: LeftCompletion
    right: RightCompletion


class JoinedActivation(Activation):
    work: JoinedWork
    prerequisite: BranchesCompleted
```

There is no workflow condition saying:

```text
if left_complete and right_complete:
    run(joined)
```

The prerequisite for `JoinedActivation` **is**:

```text
LeftCompletion × RightCompletion
```

The legal execution structure is part of the program.

```text
              BeginningCompletion
                      │
              ┌───────┴───────┐
              ▼               ▼
       LeftActivation    RightActivation
              │               │
              ▼               ▼
       LeftCompletion    RightCompletion
              └───────┬───────┘
                      ▼
             BranchesCompleted
                      │
                      ▼
              JoinedActivation
```

---

## Execution is algebra, not hidden orchestration

`ontok-ex` represents each reachable execution state as a type.

An execution can be requested, have its beginning completed, wait for either branch, join after either branch order, or become terminal.

Arriving completion facts construct the next legal state and the new fact that became true.

Conceptually:

```text
current execution proof + arriving fact
                    │
                    ▼
             execution fold
                    │
              ┌─────┴─────┐
              ▼           ▼
         next state     emission
```

The runtime does not need to rediscover the workflow from configuration or ask an intelligent controller what should happen next.

The program already declares the legal relationships.

Transport can carry execution requests, activations, and completions without owning their semantics. Workers can perform Work without owning the state machine. Models can perform inference inside Work without deciding the legal control flow.

**ONTOK can own the execution semantics without owning the runtime.**

The terminal execution also preserves the path that produced it: the originating request, activations, completions, prerequisites, and outcomes remain part of the immutable proof.

---

## One kernel, multiple capabilities

Execution is one consequence of making organizational meaning explicit.

ONTOK grows through modules rather than expanding Core into a universal enterprise model.

```text
                    ONTOK Core
                         │
        ┌────────────────┼────────────────┐
        ▼                ▼                ▼
       EX               ST               VSM
   execution      semantic topology   value streams

                         │
                        SCIM
                   identity semantics
```

`ontok-ex` expresses execution over declared Work and organizational meaning.

`ontok-st` represents the evolving relationships among independently developed Concepts.

`ontok-vsm` represents value-stream structure and performed work through the same organizational grammar.

`ontok-scim` aligns standardized identity structures with the broader organizational model.

Organizations can build their own modules the same way.

A useful concept does not need to become universal before it can participate in the system.

---

## Specification and realization

ONTOK is not defined by Python.

Each module has an implementation-independent specification describing its semantics, refinements, constraints, and dependencies.

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
 executable model
```

The specifications are currently expressed in XML.

The first realization is Python, using strict Pydantic models so ONTOK kinds and facts can participate directly in ordinary application code.

Established standards can be used where interoperability benefits from them. RDF, OWL, SHACL, SKOS, SCIM, graph platforms, and other representations may project or exchange ONTOK semantics without becoming ONTOK's programming model.

The specification defines the language.

A realization makes it usable.

---

## Use ONTOK

The Python realization is maintained as a `uv` workspace under:

```text
packages/python/
```

The repository contains Core, extensions, implementation-independent specifications, examples, tests, and module documentation.

Start with Core to understand the language, then inspect the modules relevant to the problem you are solving:

```text
ontok-core    semantic kernel
ontok-ex      execution
ontok-st      semantic topology
ontok-vsm     value streams
ontok-scim    identity
```

ONTOK does not require the organization to become one application, one graph, or one ontology.

It gives those systems a language in which their meaning can become explicit, related, validated, and operated on as software.

**Write the organization as software.**

---

## License

ONTOK is licensed under the [Apache License 2.0](LICENSE).
