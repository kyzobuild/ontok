# The Ontological Organization 

## Reference Architecture

## **ONTOK as the Semantic Kernel of the Enterprise**

### **Position**

The Ontological Organization paper establishes the hypothesis: an organization is a knowledge system, and its canonical schema is an ontology that must become explicit, stable, and executable. ONTOK establishes the kernel: the ten primitives from which arbitrary knowledge can be constructed. This document defines the formal architecture that results when the two are composed. The paper answers why. ONTOK answers what. This answers how.

The composition is not decorative. The paper's six-layer model becomes formally specifiable the moment the ontology layer has a kernel, because every other layer can then be defined in terms of kernel operations. Alignment becomes claim construction. Projection becomes compilation. Agency becomes a typed execution loop over the primitives. The architecture stops being a diagram and becomes a system with invariants.

### **The Formal Object**

The organizational knowledge system is defined as:

```
O = (K, D, M, S, Pi, X)
```

where:

**K** is the semantic kernel: ONTOK's ten primitives (Entity, Event, State, Role, Relation, Claim, Evidence, Context, Concept, Rule) plus the construction pipeline (Evidence to Claims to structured knowledge to domain concepts to derived knowledge). K is small, versioned, and governed like an ABI. It changes rarely and never silently.

**D** is the set of domain ontologies. Each domain ontology is a specialization of K and only a specialization of K. Customer specializes Entity. Contract signing specializes Event. Strategic classification specializes State scoped to a Context. Contractual obligation specializes Rule. Account ownership specializes Role. Domains compose primitives; they never extend the primitive set. This is the kernel closure property, and it is what keeps a healthcare ontology and a financial ontology mutually intelligible.

**M** is the alignment layer: the set of mappings from existing enterprise representations (schemas, semantic models, API contracts, documents, workflow definitions, authorization structures) to domain concepts.

**S** is the knowledge substrate: the persistence and derivation engine holding the constructed knowledge.

**Pi** is the projection compiler: the set of functions that generate purpose-specific artifacts from O. Each artifact A\_i \= Pi\_i(O).

**X** is the actor runtime: humans, deterministic services, and agents, all operating against O through a common action protocol.

### **The Self-Hosting Property**

The single most important formal move in this architecture is that the alignment layer M is expressed in the kernel's own primitives.

A mapping such as "cust\_no in the billing system refers to the Customer concept" is not configuration metadata living in a special mapping database. It is a Claim. Its Evidence is the schema definition, the data profile, and the record of SME validation. Its Context is the source system and the period of validity. Its lifecycle (proposed, supported, contradicted, deprecated) is the standard Claim lifecycle.

This means the architecture describes its own adoption process. Ontology discovery is not a separate methodology bolted onto the system; it is the system's normal knowledge construction pipeline pointed at the technology estate itself:

**Discovery:** LLM extraction over representations produces candidate alignment Claims  
**Validation:** domain experts supply Evidence that promotes or rejects Claims  
**Growth:** promoted Claims extend D and M; contradicted Claims are retained with status

Brownfield adoption therefore requires no privileged machinery. The first domain the ontology models is the enterprise's own representational landscape, and every subsequent domain uses the identical pipeline. The kernel bootstraps the organization the way a compiler bootstraps itself.

### **Plane Architecture**

The system decomposes into six planes. Planes 0 through 2 define meaning. Planes 3 through 5 execute it.

**Plane 0: Kernel (K).** ONTOK's ten primitives, their type definitions, and the construction pipeline. Governance is deliberately heavy: kernel changes are versioned, reviewed, and rare. In TCA terms, the kernel types are the trusted base. Everything above them is constructed; nothing above them is assumed.

**Plane 1: Domain Ontologies (D).** Specializations composed from kernel primitives, organized per business domain and elaborated incrementally, one business outcome at a time. Domains own their vocabulary. The kernel owns the semantics of identity, occurrence, condition, participation, connection, assertion, support, scope, classification, and constraint.

**Plane 2: Alignment (M).** Claims connecting existing representations to domain concepts, with Evidence and Context, produced by the discovery pipeline and validated by humans. Source systems are never modified to conform. Meaning is layered over implementation.

**Plane 3: Knowledge Substrate (S).** The persistence and derivation engine. The architecture is implementation-agnostic in principle, but the kernel's operations impose real requirements that eliminate most naive implementations:

*Bitemporality.* State carries valid time (when the condition held in the world). Claim carries assertion time (when the system came to believe it). The separation is mandatory because the enterprise question "what did we believe on March 3 about what was true on January 1" is not exotic; it is every audit, every dispute, every postmortem.

*Append-only evidence.* Evidence and Claims are never deleted. Belief revision is a status transition on a Claim, not a destructive update. History is preserved by construction, which is the property that makes the system explainable after the fact.

*Recursive derivation.* Rules derive conclusions from facts and other conclusions. Claims revise claims. Identity resolution depends on relationships that are themselves derived. These are recursive queries over facts, which is why a declarative Datalog-class engine is the natural substrate and why a conventional CRUD store is not. The substrate must evaluate rules, not merely retrieve rows.

*Canonical identity.* Entity resolution requires stable, comparable identity across sources. Canonical encoding at the substrate level (byte order equals value order) makes identity and ordering properties of construction rather than conventions of application code.

**Plane 4: Projection Compiler (Pi).** Projections are compiled from O, not modeled independently. Each projection selects a subset of the ontology and transforms it into an artifact a downstream system consumes:

**Pi\_context(O, objective, actor)**  \-\> agent context graph \+ allowable actions  
**Pi\_retrieval(O, objective)**           \-\> retrieval scope (entities, relations, time bounds)  
**Pi\_semantic(O, domain)**           \-\> analytical semantic model  
**Pi\_authz(O, actor, resource)**     \-\> authorization decision  
**Pi\_schema(O, domain)**             \-\> database or API schema  
**Pi\_workflow(O, process)**           \-\> states, transitions, constraints

Two projections deserve emphasis because they fall out of the kernel with almost no additional machinery.

Authorization is Relation traversal plus Rule evaluation. Relationship-based access control (the Zanzibar family) is exactly this computation, which means the ontology does not need a parallel permission model. The same Relations that give an agent context also determine what the agent may touch, evaluated by the same Rule engine. One model, two projections.

Agent context is a compiled artifact, not a prompt-engineering craft product. Given an objective and an actor, the compiler resolves the relevant subgraph, the applicable Rules, the authoritative Evidence, and the permitted actions, and serializes them into the context window. Serialization is where SIT operates: type names, field names, and schema structure are chosen as instructions to the model, so the schema itself teaches the consuming LLM how to interpret the knowledge it receives. The context window becomes a typed view over O rather than an assembled pile of retrieved text.

**Plane 5: Actor Runtime (X).** Humans, deterministic services, and agents share one action protocol. The agent execution cycle maps onto kernel primitives exactly:

**observe**   \-\> new Evidence enters the pipeline  
**resolve**    \-\> Context is compiled via Pi\_context (Relations traversed, Evidence attached)  
**reason**     \-\> the probabilistic layer proposes candidate Claims and candidate actions  
**gate**         \-\> Rules are evaluated deterministically over the proposal  
**act**            \-\> an admitted action executes and is recorded as an Event  
**settle**       \-\> the Event transitions States, and resulting observations re-enter as Evidence

The loop is closed: the agent's inputs and outputs are both expressions in the kernel. An enterprise running this architecture is a knowledge system that updates itself as a side effect of doing its work.

### **The Deterministic Gate and Action-as-Proof**

The gate step carries the architecture's answer to the probabilistic-systems problem, and it is worth stating precisely.

The probabilistic layer (an LLM, an analytical model, a human intuition) may interpret, synthesize, and propose. It may never admit. Admission is the deterministic evaluation of the applicable Rules against the proposed action within its resolved Context, executed by the substrate's rule engine, producing a derivation trace.

This yields the architecture's strongest property: an admitted action carries a proof of its own permission. The derivation trace (these Rules, over these Relations and States, supported by this Evidence, in this Context, at this time) is constructed before execution and recorded with the resulting Event. Construction-as-proof, applied at the action level. The audit trail is not reconstructed after the fact from logs; it is the residue of the admission computation itself.

This is the precise boundary between what generative systems are good at and what enterprises require. Interpretation is probabilistic. Permission is derived. Nothing probabilistic ever sits in the admission path.

### **Invariants**

The architecture is defined by its laws more than by its components. An implementation conforms if and only if it maintains:

1. **Kernel closure.** Domain ontologies specialize K; they never extend the primitive set. Every domain type reduces to kernel primitives by construction.  
2. **Evidence grounding.** No Claim exists without at least one Evidence reference and a Context. Enforced at the type level: the unsupported claim is unrepresentable, not merely discouraged.  
3. **Non-destructive revision.** Evidence and Claims are append-only. Revision is status transition. History is total.  
4. **Bitemporal separation.** Valid time and assertion time are distinct and both queryable.  
5. **Deterministic admission.** Every state-changing action passes the Rule gate, and the gate is free of probabilistic components.  
6. **Provenance totality.** Every derived conclusion is traceable through its derivation to Claims, and through Claims to Evidence.  
7. **Projection consistency.** All artifacts consumed by downstream systems are generated or validated against O. A projection that cannot be traced to the ontology is a legacy representation awaiting alignment, and is marked as such.

Invariants 2, 3, and 6 are the trust story. Invariant 5 is the safety story. Invariants 1 and 7 are the coherence story. Invariant 4 is the audit story.

### **Type-Driven Implementation**

TCA supplies the implementation discipline for the entire stack. Kernel primitives are the foundational type family. Domain concepts are constructed types whose constructors enforce kernel invariants, so an instance existing is proof its constraints held. Illegal knowledge states (a Claim without Evidence, a State without an interval, a Relation without typed endpoints) are unrepresentable rather than validated against.

The same types serve three consumers. The substrate persists them. The rule engine evaluates over them. The projection compiler serializes them, with SIT governing the serialization so that machine-facing schemas carry their own semantics into the models that consume them. One type system, three surfaces, no translation layers where meaning can silently diverge.

### **Conformance Without Prescription**

The architecture prescribes invariants, not products. A conforming implementation might persist to a Datalog engine, a property graph, a relational system with a derivation layer, or a purpose-built substrate. It might run agents on any orchestration framework. What it may not do is violate the laws: extend the kernel from a domain, hold an ungrounded Claim, destroy history, admit an action probabilistically, or ship a projection that answers to no ontology.

The result is the enterprise the original paper hypothesized: a knowledge system in continuous operation, whose ontology is explicit, whose meaning is layered over its existing systems rather than replacing them, whose agents act inside the model rather than outside it, and whose every action arrives carrying the proof that it was permitted.

### **Open Questions**

Three questions are genuinely open and stated as such. Whether ten primitives is the correct kernel cardinality, or whether operational pressure will demand a split (Observation from Evidence) or a merge (Role into Relation). What the default contradiction policy should be when Claims conflict and no Rule adjudicates. And how much of Plane 2 discovery can be promoted without human validation as extraction confidence becomes measurable. The kernel's governance model exists precisely so these questions can be answered slowly.

