# The Ontological Organization 

## Reference Architecture

## **ONTOK as the Semantic Kernel of the Enterprise**

### **Position**

The Ontological Organization paper establishes the hypothesis: an organization is a knowledge system, and its canonical schema is an ontology that must become explicit, stable, and executable. ONTOK establishes the kernel: twelve statement-function kinds and the laws that make statements built by independent systems mechanically commensurable. This document defines the formal architecture that results when the two are composed. The paper answers why. ONTOK answers what. This answers how.

The composition is not decorative. The six-plane model — introduced here, in this document — becomes formally specifiable the moment the ontology layer has a kernel, because every other plane can then be defined in terms of kernel judgments. Alignment becomes classification. Projection becomes compilation. Agency becomes a typed execution loop over the twelve kinds. The architecture stops being a diagram and becomes a system with invariants.

### **The Formal Object**

The organizational knowledge system is defined as:

```
O = (K, D, M, S, Pi, X)
```

where:

**K** is the semantic kernel: ONTOK's twelve statement-function kinds — entity, event, state, role, relation, claim, evidence, derivation, invalidation, rule, context, concept — together with the laws of RFC 1 that govern them: classification, formation, correspondence, grounding, release, and standing. K is small, versioned, and governed like an ABI. It changes rarely and never silently.

**D** is the set of domain ontologies. A domain ontology is vocabulary — predicates and referents — plus the concept statements that classify each predicate to exactly one kernel kind. A billing predicate such as cust\_no is classified through the domain concept customer, which is classified as entity-functioning; a contract-signing predicate is classified as event-functioning; an obligation predicate as rule-functioning; an ownership predicate as role-functioning. Domains compose statements of the twelve kinds; they never add kinds, and no domain thing subtypes a kernel kind. This is the kernel closure property, and it is what keeps a healthcare ontology and a financial ontology mutually intelligible.

**M** is the alignment layer: concept statements aligning existing enterprise representations (schemas, semantic models, API contracts, documents, workflow definitions, authorization structures) to domain concepts, each grounded by claims and evidence and scoped by context. A mapping is not configuration metadata; it is an ordinary statement in the graph.

**S** is the knowledge substrate: the persistence and derivation engine holding the constructed knowledge.

**Pi** is the projection compiler: the set of functions that generate purpose-specific artifacts from O. Each artifact A\_i \= Pi\_i(O).

**X** is the actor runtime: humans, deterministic services, and agents, all operating against O through a common action protocol.

### **The Self-Hosting Property**

The single most important formal move in this architecture is that the alignment layer M is expressed in the kernel's own kinds.

A mapping such as "cust\_no in the billing system refers to the Customer concept" is not configuration metadata living in a special mapping database. It is a concept statement: cust\_no, classified to the customer concept. Its grounds are ordinary statements about it: a claim that an analyst asserts it, evidence that the billing schema definition and the data profile bear it. Its scope is ordinary context: the source system, the period of validity. Its lifecycle — proposed, supported, contradicted, withdrawn — is not a status field but the computed standing of its grounds and the invalidations that release them.

This means the architecture describes its own adoption process. Ontology discovery is not a separate methodology bolted onto the system; it is the system's normal knowledge construction pipeline pointed at the technology estate itself:

**Discovery:** extraction over representations produces candidate grounded mappings: a concept statement aligning a source predicate to a domain concept, the claim that asserts it, and whatever evidence the extractor can cite. A candidate is ordinary graph content awaiting admission, not a privileged object.
**Validation:** a domain expert adds evidence that grounds a candidate further, or an invalidation that releases its claim. Validation changes grounds only; a candidate is formed exactly as every other statement is formed, and claim formation remains the kernel's, unchanged.
**Growth:** admitted grounded alignments extend D and M; contradicted alignments remain in the graph — standing is computed, never stored

Brownfield adoption therefore requires no privileged machinery. The first domain the ontology models is the enterprise's own representational landscape, and every subsequent domain uses the identical pipeline. The kernel bootstraps the organization the way a compiler bootstraps itself.

### **Plane Architecture**

The system decomposes into six planes. The six-plane model originates in this document: ONTOK specifies K and its laws and nothing else, and the planes are this architecture's decomposition of everything the kernel does not own. Planes 0 through 2 define meaning. Planes 3 through 5 execute it.

**Plane 0: Kernel (K).** The twelve statement-function kinds and the laws of RFC 1, nothing more. Governance is deliberately heavy: kernel changes are versioned, reviewed, and rare. The kernel assumes nothing above it, and everything above it is constructed from statements of the twelve kinds.

**Plane 1: Domain Ontologies (D).** Domain vocabularies classified through concept statements, organized per business domain and elaborated incrementally, one business outcome at a time. Domains own their vocabulary. The kernel owns the semantics of identity, occurrence, condition, participation, connection, assertion, support, inference, release, constraint, scope, and classification — the twelve functions a statement can perform.

**Plane 2: Alignment (M).** Concept statements connecting existing representations to domain concepts, grounded by claims and evidence, scoped by context, produced by the discovery pipeline and validated by humans. Source systems are never modified to conform. Meaning is layered over implementation.

**Plane 3: Knowledge Substrate (S).** The persistence and derivation engine. S owns persistence, bitemporality, identity, derivation execution, and admission: every statement the system holds is persisted by S, every rule is evaluated by S, and every proposal is admitted or refused by S. The architecture is implementation-agnostic in principle, but the kernel's operations impose real requirements that eliminate most naive implementations:

*Bitemporality.* Valid time (when a condition held in the world) and assertion time (when the system came to believe it) are both context, attached at different levels of the graph: a context statement scopes the state; another context statement scopes the ground. The kernel has no clock; temporal ordering belongs to the domains and the realization. The separation is mandatory because the enterprise question "what did we believe on March 3 about what was true on January 1" is not exotic; it is every audit, every dispute, every postmortem.

*Append-only statements.* No statement is ever deleted. Belief revision is the admission of an invalidation releasing one ground — never a destructive update, never a stored status. History is preserved by construction, which is the property that makes the system explainable after the fact.

*Recursive derivation.* Rules derive conclusions from facts and other conclusions. Claims ground statements whose grounds are themselves derived. Identity resolution depends on relationships that are themselves derived. These are recursive queries over facts, which is why a declarative Datalog-class engine is the natural substrate and why a conventional CRUD store is not. The substrate must evaluate rules, not merely retrieve rows. The requirement is normative; Datalog is not — any engine that evaluates recursive rules over the graph satisfies it.

*Canonical identity.* Entity resolution requires stable, comparable identity across sources. Canonical encoding at the substrate level (byte order equals value order) makes identity and ordering properties of construction rather than conventions of application code. Non-normative: any encoding with the same determinism satisfies the requirement.

**Plane 4: Projection Compiler (Pi).** Pi owns compilation. Projections are compiled from O, not modeled independently. Each projection selects a subset of the ontology and transforms it into an artifact a downstream system consumes:

**Pi\_context(O, objective, actor)**  \-\> agent context graph \+ allowable actions  
**Pi\_retrieval(O, objective)**           \-\> retrieval scope (entities, relations, time bounds)  
**Pi\_semantic(O, domain)**           \-\> analytical semantic model  
**Pi\_authz(O, actor, resource)**     \-\> authorization decision  
**Pi\_schema(O, domain)**             \-\> database or API schema  
**Pi\_workflow(O, process)**           \-\> states, transitions, constraints

Formally, a projection is a function from an identified source subgraph of O and an identified rule set to an artifact, and traceability is part of the output: every projection artifact records the graph it was compiled from and the rules that governed its compilation. An artifact that identifies neither is not a projection; it is a legacy representation awaiting alignment.

Two projections deserve emphasis because they fall out of the kernel with almost no additional machinery.

Authorization is Relation traversal plus Rule evaluation. Relationship-based access control (the Zanzibar family) is exactly this computation, which means the ontology does not need a parallel permission model. The same Relations that give an agent context also determine what the agent may touch, evaluated by the same Rule engine. One model, two projections.

Agent context is a compiled artifact, not a prompt-engineering craft product. Given an objective and an actor, the compiler resolves the relevant subgraph, the applicable Rules, the authoritative Evidence, and the permitted actions, and serializes them into the context window. Serialization is itself a compilation decision owned by Pi: type names, field names, and schema structure are chosen as instructions to the model, so the schema itself teaches the consuming LLM how to interpret the knowledge it receives. The context window becomes a typed view over O rather than an assembled pile of retrieved text.

**Plane 5: Actor Runtime (X).** X owns the action protocol and execution. Humans, deterministic services, and agents share one action protocol; admission itself remains S's function, invoked through the protocol. The agent execution cycle maps onto kernel kinds exactly:

**observe**   \-\> new Evidence enters the pipeline  
**resolve**    \-\> Context is compiled via Pi\_context (Relations traversed, Evidence attached)  
**reason**     \-\> the probabilistic layer proposes candidate Claims and candidate actions  
**gate**         \-\> Rules are evaluated deterministically over the proposal  
**act**            \-\> an admitted action executes and is recorded as an Event  
**settle**       \-\> the Event transitions States, and resulting observations re-enter as Evidence

The loop is closed: the agent's inputs and outputs are both expressions in the kernel. An enterprise running this architecture is a knowledge system that updates itself as a side effect of doing its work.

### **The Deterministic Gate and Action-as-Proof**

The gate step carries the architecture's answer to the probabilistic-systems problem, and it is worth stating precisely as four distinct stages.

**Proposal.** The probabilistic layer (an LLM, an analytical model, a human intuition) may interpret, synthesize, and propose. A proposal is ordinary graph content — candidate statements, grounded by the claim that the proposer asserts them — and it changes nothing authoritative. It may never admit.

**Admission.** Admission belongs to S: the deterministic evaluation of the applicable rules against the proposed action within its resolved context, executed by the substrate's rule engine. The evaluation is itself kernel content — a rule statement, a derivation statement citing that rule, relation statements attaching the derivation's inputs, the evidence grounding those inputs, and the context scoping the decision. No probabilistic component sits in this stage.

**Execution.** An admitted action — and only an admitted action — is executed by X through the action protocol.

**Recording.** The executed action is recorded as an event, its resulting condition as a state, and the admission trace is recorded beside them. The trace exists before the event; the event does not assert its own permission — the derivation carries it.

This yields the architecture's strongest property: an admitted action carries a proof of its own permission. Construction-as-proof, applied at the action level. The audit trail is not reconstructed after the fact from logs; it is the residue of the admission computation itself.

This is the precise boundary between what generative systems are good at and what enterprises require. Interpretation is probabilistic. Permission is derived. Nothing probabilistic ever sits in the admission path, and no probabilistic output becomes authoritative state directly: it enters as a proposal and becomes state only through admission, execution, and recording.

### **Invariants**

The architecture is defined by its laws more than by its components. An implementation conforms if and only if it maintains:

1. **Kernel closure** (Planes 0–1). Domain ontologies classify their vocabulary through K; they never add kinds. Every domain predicate reaches exactly one kernel kind through concept statements.
2. **Evidence grounding** (Plane 3, admission policy). No statement is admitted without at least one ground and a context scope. This is admission policy owned by this architecture, not a kernel law: the kernel permits an ungrounded claim; this architecture does not admit one.
3. **Non-destructive revision** (Plane 3). The graph is append-only. Revision is the invalidation of one ground; standing is recomputed, never stored. History is total.
4. **Bitemporal separation** (Plane 3, with Plane 1 vocabulary). Valid time and assertion time are distinct context scopes — over states and over grounds respectively — and both are queryable.
5. **Deterministic admission** (Plane 3, invoked by Plane 5). Every state-changing action passes the Rule gate, the gate is free of probabilistic components, and every admitted action carries its complete derivation trace: rule, derivation, inputs, evidence, context.
6. **Provenance totality** (Plane 3). Every derivation cites its rule, and every standing statement is traceable through its active grounds to claims, evidence, and further derivations.
7. **Projection consistency** (Plane 4). All artifacts consumed by downstream systems are generated or validated against O, and every projection identifies its source graph and compilation rules. A projection that cannot be traced to the ontology is a legacy representation awaiting alignment, and is marked as such.

Invariants 2, 3, and 6 are the trust story. Invariant 5 is the safety story. Invariants 1 and 7 are the coherence story. Invariant 4 is the audit story.

### **Type-Driven Implementation**

The reference realization is type-driven across the entire stack. The kernel's formation rules are the foundational type family: each of the twelve kinds is a type whose constructors admit exactly the position occupancies RFC 1 assigns it. Domain predicates are classified at construction, so a statement's kind is computed from its predicate and can never be supplied by a caller. Kernel-illegal statements — a literal in a predicate position, a derivation whose value is not a rule, an invalidation whose subject is not a ground — are unrepresentable rather than validated against.

The same types serve three consumers. The substrate persists them. The rule engine evaluates over them. The projection compiler serializes them, treating names and structure as instructions to the consuming model, so that machine-facing schemas carry their own semantics into the models that consume them. One type system, three surfaces, no translation layers where meaning can silently diverge.

### **Conformance Without Prescription**

The architecture prescribes invariants, not products. A conforming implementation might persist to a Datalog engine, a property graph, a relational system with a derivation layer, or a purpose-built substrate. It might run agents on any orchestration framework. What it may not do is violate the laws: extend the kernel from a domain, admit an ungrounded statement, destroy history, admit an action probabilistically, or ship a projection that answers to no ontology. Nor does the architecture itself extend the kernel: every plane composes the twelve kinds and adds none.

The result is the enterprise the original paper hypothesized: a knowledge system in continuous operation, whose ontology is explicit, whose meaning is layered over its existing systems rather than replacing them, whose agents act inside the model rather than outside it, and whose every action arrives carrying the proof that it was permitted.

### **Open Questions**

Two questions are genuinely open and stated as such. What the default contradiction policy should be when conflicting statements both stand and no rule adjudicates. And how much of Plane 2 discovery can be promoted without human validation as extraction confidence becomes measurable. The kernel's closure is settled by RFC 1 and is not an architecture question; the architecture's governance model exists so these remaining questions can be answered slowly.
