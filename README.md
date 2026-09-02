# ONTOK

ONTOK is a modular declarative programming language for making the organization itself programmable. Its small universal core defines how people, software, agents, resources, conditions, actions, meanings, and rules compose as one organizational graph; optional modules add standard organizational capabilities without enlarging that core.

## What Is an Organization?

An organization is a persistent constitutive order that gives one identity and agency to changing physical, social, digital, and abstract particulars. It joins them through explicit typed Connections and coordinates their capacities and actions toward organizational ends. Its identity persists when each successive configuration is recognized as the lawful continuation of the previous one.

## Modules

Each implementation-independent XML specification defines one ONTOK module:

- **Core** defines the universal organizational type system.
- **VSM** defines value streams as function-like compositions of organizational action.
- **SCIM** aligns standard identity resources with the organizational graph.

Further modules can add independently adoptable capabilities through explicit one-way dependencies.

## The Organizational Graph

Everything represented is exactly one of:

- **Node** — a distinct thing represented in the organizational graph.
- **Connection** — a typed link declaring how Nodes relate within the organizational graph.

From this structure, each successive layer requires constructs supplied by the layers before it.

### Reality

- **Entity** — a particular thing whose identity persists as its conditions and associations change.
- **Relation** — an identifiable domain association from one Node to another.
- **State** — a condition of a Node that holds within the organizational graph.
- **Event** — a durable memorial of one organizational occurrence.

Every Reality construct carries explicit type identity. An Event declares its temporal extent and memorialization; its recording time follows from those constructed facts, while causation exists separately as a typed Relation between Events. Concrete Event types name their participants and occurrence-specific facts directly.

### Agency

- **Role** — a capacity through which an Entity acts.
- **Goal** — an intended State.
- **Action** — intentional activity performed or attempted by an Entity through a Role toward a Goal and memorialized by an Event.

### Meaning

- **Concept** — what gives a declaration meaning through type identity, semantic refinement, and explicit alignment.
- **Context** — the States under which meaning or action applies.

### Governance

- **Rule** — what determines whether an Action is required, permitted, or prohibited within a Context.

## The Operating Cycle

States describe present conditions, Goals identify intended States, and Entities act through Roles toward those Goals. Every Action is memorialized by an Event whose concrete type and fields describe what occurred.

Concepts determine what declarations mean, Contexts determine where meaning and action apply, and Rules govern Actions within those Contexts. Explicit Connections bind every declaration beneath the same organizational identity and constitutive order, making one coherent executable graph rather than separate descriptions.

## Reference Implementation

Language realizations live beneath `packages/<language>/`, allowing each language to use its native workspace and packaging tools while implementing the same semantic modules.

The Python realization is organized under `packages/python/` as a uv workspace of independently publishable packages sharing the `ontok` namespace:

- `ontok-core` provides `ontok.core`.
- `ontok-vsm` provides `ontok.vsm` and depends on `ontok-core`.
- `ontok-scim` provides `ontok.scim` and depends on `ontok-core`.

Core implementation proceeds one completed semantic layer at a time; extension packages remain empty until their specifications and Core dependencies are complete.

The XML specification and its package evolve as one executable specification: XML defines meaning independently of Python, while construction through the Python types proves that a declaration satisfies that meaning.