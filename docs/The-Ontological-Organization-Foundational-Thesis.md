# The Ontological Organization

## Foundational Thesis 

*by Kyle Tobin*

## The decision that lives nowhere

An organization cannot operate without a model of what it knows. It must know the concepts its work depends on and the relationships that hold between them. That model is an ontology, and it is the blueprint the organizational machine runs on. We project fragments of the blueprint into tools across the digital and physical world, but the foundational machinery required to run our organizations is still the mind.

Consider an ordinary business situation. A strategic customer is experiencing an unresolved production incident on a contractually critical service, and someone decides the account should be reviewed before the next executive meeting.

Now ask where that decision lives.

The customer's identity is in the CRM. The strategic classification came out of an account planning process. The contract terms are in a document repository. The service dependency is mapped, loosely, in a configuration management platform. The incident is a ticket. The executive meeting is a calendar entry. Every fact has a system. But the rule that connects them, the rule that says these facts together demand action, is encoded nowhere. It exists only in the head of an account manager or a support rep or an executive who has seen this before.

The organization functions anyway. It functions because a person reassembled the model on demand. They recognized which facts belong together, knew which source was authoritative, applied a rule no one ever wrote down, and inferred what should happen next. That reassembly is performed thousands of times a day in every company on earth, and it is so ordinary that enterprise architecture has never treated it as a system component.

It should, because it is one. People are the middleware. For the entire history of enterprise computing, people have served as the semantic integration layer: the component that reconciles inconsistent terminology, resolves identity across systems, supplies missing business rules, and translates fragments into meaning. Every organization already has an ontology, a coherent model of what exists, how it relates, and what governs it. It has simply never needed to be written down, because it has been running on people.

Treat that claim as engineering rather than metaphor and its implications sharpen. This layer is undocumented, so no one can inspect the rules it applies. It is unversioned, so no one knows when a rule changed or why. It replicates only through years of proximity, and when a person leaves, the portion of the model they carried leaves with them. No architect would design a critical system this way. Every organization runs one, because it came free with the workforce, and because for a hundred years there was no alternative.

The arrangement worked, which is why nobody noticed it.

## The graveyard is evidence

Some people did notice. Herbert Simon described organizations as information processing systems whose real structure lies in how knowledge and decisions flow rather than in how the boxes are drawn. Conway observed that the systems an organization builds mirror the communication structure of the people who build them, which is another way of saying that the seams in our software trace the seams in the implicit layer. The sociotechnical tradition spent decades arguing that the boundary between people and machines is the most consequential design surface in any enterprise. The layer was seen, named, and studied.

And practitioners tried to build the explicit version. The semantic web. Master data management. Data governance councils. Twenty years of knowledge graph vendors promising a unified model of the business. Most of it went nowhere, and every experienced architect knows it, which is why the word ontology now provokes justified suspicion in anyone who controls a budget.

The theorists and the practitioners were not defeated by flaws in the idea. They were defeated by economics. People supplied the semantics invisibly, as a byproduct of doing their jobs, at a marginal cost of zero. Against free, invisible, and good enough, an explicit model could only ever be justified as pure cost. There was no failure mode that formalization prevented, because the implicit layer quietly prevented those failures first. Every ontology initiative was therefore asked to prove value against a competitor that never appeared on any diagram and never missed a day of work. The explicit model died in committee every time, for structural reasons that had nothing to do with its correctness.

The graveyard is not an embarrassment for this idea. It is evidence. The idea was early. And an idea that is early becomes an idea that is right at the moment its blocking constraint disappears. The constraint, to be exact, was this: every worker who ever needed the implicit model could acquire it from the people who held it. That constraint has now failed.

## Agents are the forcing function

Large language models and agentic systems change the relationship between software and organizational knowledge in one specific, structural way: agents do work that crosses application boundaries, and they cross those boundaries without the tacit context that people carry across them.

Traditional software never had this problem because it never had this ambition. A CRM manages customer relationships. A ticketing system manages incidents. Each application owns a bounded slice of meaning, and the seams between slices are stitched by people. An agent is asked to fulfill an objective, not operate an application. Prepare for the customer meeting. Investigate the supply disruption. Assess the renewal risk. Fulfilling the objective requires traversing many systems, and the moment the agent crosses its first boundary, it needs exactly the thing no system contains: the model that connects an incident to a service, the service to a contract, the contract to a customer, the customer to a strategic classification, and all of it to a rule about what should happen next.

The instinctive remedy is more integration. Wire the agent to the CRM, the ticketing system, the document store, the calendar. This does not work. Connectivity provides access. Semantics provide meaning. Retrieval can surface the emails, the tickets, and the contract clauses, but nothing in those artifacts establishes that this incident affects that service governed by this contract owned by that person. Those are relationships, and relationships are precisely what the implicit ontology encodes and the application landscape does not.

Consider how every previous worker solved this same problem, because every previous worker faced it. No new hire arrives knowing which source is authoritative, which rules are real, or which exceptions matter. People close that gap through apprenticeship. They work near the people who hold the model, absorb it through observation and correction, and within months the implicit layer has replicated itself into one more mind. Apprenticeship is the deployment mechanism of the implicit ontology, and it is the mechanism agents cannot use. An agent can inherit only what has been written down.

This is the clean explanation for a pattern operations leaders are living through right now: the disappointing agent pilot. The agent was deployed onto an existing workflow and underperformed, and the postmortem blamed the model. But the process was only ever half written. The other half lived in people, and every prior hire had closed that gap through apprenticeship to the people who held it. The agent arrived with no one to apprentice to and only the written half of a half-written process. The failure was structural, and it will repeat at every organization that deploys before it declares.

## Applications are projections, not models

If the remedy is declaration, it matters enormously what is being declared, because the graveyard is full of programs that declared the wrong thing.

Once you see the organization as a knowledge system, the technology estate looks different. No application models the enterprise. Each one models a purpose-specific slice of it. The CRM is a projection of the organization's knowledge centered on commercial relationships. The ERP is a projection centered on transactions and obligations. The analytics semantic model is a projection built for measurement. The org chart, which executives often mistake for the definitive model of the company, is a projection too. It captures formal authority and reporting lines while omitting the networks of customer ownership, expertise, service dependency, and decision authority through which value actually moves.

These projections overlap without agreeing. A customer, an account, a subscriber, and a member may be the same concept, related concepts, or different concepts depending on which system you ask. People reconcile the differences constantly, which is why the inconsistency has always been survivable.

The practical consequence of the projection view is that fixing the inconsistency does not mean replacing anything. A source system can keep calling its field cust\_no forever. What organizations need is not a universal schema imposed on every system but a semantic alignment layer: an explicit statement that cust\_no refers to the Customer concept, that FactSupportCase records events affecting a Service, that this approval workflow implements that policy. Every experienced analyst already carries these statements. Writing them down changes nothing about the systems and everything about what can operate across them. Implementations stay local. Meaning becomes shared. That separation is what makes the approach viable in a brownfield enterprise, which is to say every enterprise. It is also why the prior failures do not predict this one. Those programs asked systems and teams to change what they do. This asks them only to declare what they mean.

## Automation is refactoring, not substitution

Here the argument turns from architecture to organization, and it gets uncomfortable.

The dominant mental model for agentic transformation is substitution. Inventory the tasks people perform, identify the automatable ones, assign them to agents, and keep the workflow. This model is popular because it is legible to procurement and because it preserves the org chart. It is also wrong, for an engineering reason. Existing workflows are not neutral descriptions of the work. They are artifacts of the constraints under which they were designed: cognitive limits, application boundaries, communication latency, organizational politics, and the distribution of tacit knowledge across specific people. The handoff between two departments often exists not because the work demands a handoff but because the knowledge required lives in two heads.

When the constraints change, the optimal decomposition of the work changes with them. Some tasks need to split into smaller machine operations to be observable and controllable. Several tasks collapse into one machine objective because the handoffs between them existed only to route around organizational boundaries. Sequential steps become parallel. Some activities vanish. Others become economical for the first time.

Software development is the visible preview. When generation reduced the cost of producing code, capable engineers did not simply produce more code. The boundaries that had defined the job stopped binding. An engineer with real architectural judgment is now effective in languages they have never written, because the barrier was never the judgment, it was fluency, and fluency became cheap. The person who builds the system can now decide what it should do and understand why it matters commercially, work that was divided into separate roles only because no one could hold all of it at the same time. Those roles were never natural kinds. They were partitions of one job across many heads, drawn wherever the cost of acquiring the next skill exceeded the cost of a handoff. The acquisition cost collapsed, and the partitions are collapsing with it.

That claim reaches well beyond this essay, and it deserves an argument of its own, which I intend to make. For present purposes one consequence suffices: agentic transformation is organizational refactoring, and substitution is the junior version of the idea.

## The sequence: semantics first, then work

If the workflow is up for redesign and the workflow's missing half lives in people, then the standard opening question of every AI initiative, which tasks should we automate, arrives too late. It optimizes the artifact of old constraints before understanding what the work actually is.

The foundational question is: what organizational knowledge makes this work meaningful and executable?

Answer that first. Discover the representations that already exist. Schemas, semantic models, API contracts, workflow definitions, authorization rules, policy documents. Each is evidence about the implicit ontology, and language models are unreasonably good at extracting candidate concepts and relationships from them for domain experts to validate. Then make explicit the things nothing currently encodes: the rules, the authority structures, the exceptions, the source-of-truth decisions that today exist only as judgment.

Only then model the workflow honestly and redesign it. Assign each activity deliberately to people, deterministic automation, or agents. Let probabilistic systems interpret, synthesize, and propose. Let deterministic constraints decide what is permitted, what is valid, and what actually occurred. Execute, observe, and refactor again.

Semantic refactoring, then work refactoring, then agentic execution. Every premise behind the sequence has now been established: the knowledge is real, it is implicit, agents cannot apprentice to it, and the workflows shaped around its old distribution are not sacred. Organizations running the sequence in reverse are discovering, expensively, why order matters.

## The schema was always there

None of this requires a monolithic enterprise knowledge graph, a rip-and-replace program, or a two-year modeling exercise before the first dollar of value. The semantic model should grow the way good type systems grow. You build a small, stable kernel of primitives and compose domain concepts on top, one business outcome at a time.

What it requires is a change in what enterprises consider foundational. The organization is not fundamentally a collection of applications, processes, or departments. It is a knowledge system in continuous operation, and its ontology is the canonical schema of that system. That schema has existed all along, distributed across databases, documents, and procedures, joined by the mesh of memory, and maintained by the most reliable semantic infrastructure ever deployed: people who have always understood how things fit together.

Reasoning systems are joining the workforce. They will operate beside the people and the software already there, and they arrive without the tribal knowledge that binds our tooling to our operations. Every hire before them closed that gap through apprenticeship. Reasoning systems cannot apprentice. They can inherit only what has been written down, and the organization as it stands is half written.

The model exists. It is running now, in the people who make decisions like the one this essay opened with. Making the schema explicit is the prerequisite for refactoring the enterprise to run with people, AI agents, and traditional software together. The schema was always there.

Our work is finding, understanding, and explicitly declaring that truth.

