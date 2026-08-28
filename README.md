# ONTOK

The Ontology Kernel: the closed set of ways a statement can function.

ONTOK is a notation, not an ontology. It states nothing about what exists, names no predicate, and
assumes no substrate. It applies to ontologies other people already built, the way IPA applies to
languages nobody designed for it. A statement functions the same way whether it lives in a Fabric
ontology, a PowerBI semantic model, or a spreadsheet.

The end it serves: meaning is commensurable without a mind to reconcile it.

## The model

Every statement has three positions: **subject, predicate, value**. What it holds over, what scopes
it, and what it rests on are statements about it, because a fact carries several sources and holds
in several scopes at once and a position holds one.

A position holds a **referent**, a **literal**, a **statement**, a **kind**, or **nothing**.

Twelve kinds, in declaration order:

| | | |
|---|---|---|
| **first-order** | entity, event, state, role, relation | every bound position holds a referent or a literal |
| **second-order** | claim, evidence, derivation, invalidation, rule, context | some position holds a statement |
| **reflexive** | concept | some position holds a kind |

Three of them ground a statement: claim, evidence, derivation. Invalidation releases a ground rather
than supplying one, which is why a withdrawn statement is still there and still answers.

**The kind of a statement is the kind its predicate's concept reaches.** Classify a predicate once
and every statement using it takes its kind with no further judgment. That is the whole act of
transcription, and it is why `cust_no` needs two concepts and no rewrite:

```python
from ontok import StatementConstructor

referent = lambda name: {"occupies": "referent", "name": name}

StatementConstructor.validate_python({
    "kind": "concept",
    "subject": referent("cust_no"),
    "predicate": referent("classifies"),
    "value": referent("Customer"),
})
StatementConstructor.validate_python({
    "kind": "concept",
    "subject": referent("Customer"),
    "predicate": referent("classifies"),
    "value": {"occupies": "kind", "kind": "entity"},
})
```

## Legality is representability

Each kind types its positions to exactly the occupancies its formation rule admits. A reading
outside them has no shape to be built in. Nothing rejects anything, there is no validation step
whose absence lets something through, and no rule that can be edited to admit what should have been
refused.

Construction is the only operation. Nothing evaluates, nothing reduces, nothing steps, and nothing
is stored.

## Not this model's

The value space, and what a literal may be. Which predicates a domain admits, and what each one
takes. How a statement is carried, identified, addressed, or admitted. Whether two referents are one
referent.
