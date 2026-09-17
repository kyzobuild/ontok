---
type: Reference
description: How a pure typed transformation maps proven inputs to a constructed output. Read when deriving, calculating, querying, folding, or converting program meanings.
---

# Transformation

## Use

Use when constructed inputs determine one constructed output without reading time, randomness, environment, mutable state, or an external capability.

## Required Forms

When one model owns every input, put the transformation on that model:

```python
class Fill(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    order_id: OrderId
    price: Price
    quantity: Quantity

    @property
    def exposure(self) -> Exposure:
        return Exposure(self.price.root * self.quantity.root)
```

When several meanings provide the inputs, construct a transformation model:

```python
class ApplyDiscount(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
    )
    price: Price
    discount: Discount

    @property
    def result(self) -> Price:
        return Price(self.price.root * self.discount.multiplier.root)
```

- Every input is a field on the frozen owner.
- Every semantic output is explicitly constructed.
- Equal constructed inputs produce equal outputs.
- Use `@property`; the returned Pydantic constructor proves the output on every evaluation.
- Use `@computed_field` only when the output belongs to a serialized contract.
- A derivation takes only `self` and its body is exactly one returned expression. A parameterized question is a frozen model holding its inputs, not a parameterized method.
- Use only the closed algebra below. The expression's domain rule is declared by its owning meaning, not chosen by the caller.
- Behavior that differs by union variant is a same-named typed derivation on each variant, consumed without case selection.
- A [state-transition](state-transition.md) fact that authorizes effects owns their action derivation; do not split that authorization into a caller-selected transformation or a verb-shaped wrapper around the successor constructor.

The closed algebra admits composition of Pydantic constructors, declared field and derivation reads, arithmetic over those values, a fold over a declared collection, an extremum along a declared ranked value space, selection by a proven key, and lookup of a closed vocabulary value through a total case table. A comprehension or generator is admitted only within the returned construction expression for collection construction, folding, or extrema; it has no filtering `if` clause. Recursion follows declared recursive constituents through their derivations.

A case table maps every member of a closed value vocabulary to its declared value. It is not a registry of classes, callables, union variants, or workflow steps. Key selection requires constructed membership evidence; a potentially missing lookup must have a modeled answer, never `.get()` returning `None`, a caught `KeyError`, or ordered-union trial construction inside the domain. An operation outside this algebra is a reported construction gap, not permission for free code.

## Do Not

- define a free transformation function
- read a clock, random source, environment, global, client, cache, database, or current-state pointer
- mutate an input or output
- store the output beside the fields that determine it
- return a bare primitive when the output has semantic meaning
- hide a transformation in a validator, route, interpreter, or composition root
- use `@cached_property` on a semantic model
- use local assignments, statement loops, `if`, `match`, `try`, mutation, or multiple statements in a derivation
- disguise branching as a ternary, `and`, `or`, a filtered comprehension, `isinstance`, discriminator comparison, or a dispatch dictionary
- call a lambda, private helper, callback, or uninspected method to hide an operation outside the algebra
- add a foreign lift when annotations, aliases, and nested construction already express the same meaning

## Prove

For every input union variant and collection boundary, construct the transformation twice from equal inputs and assert equal typed outputs. Inspect its syntax: only `self`, one return statement, and operations from the closed algebra; reject the forbidden statement and expression forms above. Prove case-table coverage over the declared vocabulary, key membership for selection, and nonempty input or a modeled empty case for extrema. Transitively inspect every read derivation and called constructor: reads originate in declared fields, calls stay within admitted construction and algebra operations, no program-owned custom validator or construction hook appears, and no infrastructure, clock, randomness, environment, or mutable-global dependency appears. A single expression or repeated equal test results alone do not prove these properties.
