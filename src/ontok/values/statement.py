"""The twelve kinds, as the only statements that can be spelled.

Every statement has exactly three positions: subject, predicate, value. What it holds over, what
scopes it, and what it rests on are statements about it, because a fact carries several sources and
holds in several scopes at once and a position holds one.

The predicate position holds a referent in all twelve. A concept classifies that referent, and the
kind of a statement is the kind its predicate's concept reaches. Classifying a predicate once is
therefore the whole act of transcription: every statement using it takes its kind with no further
judgment, which is how an ontology someone else already built lands here.

Each kind types its positions to exactly the occupancies its formation rule admits, so a reading
outside them has no shape to be built in. Nothing rejects anything.
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Discriminator, TypeAdapter

from ontok.values.kind import OntokKind
from ontok.values.occupancy import SEALED, Kinded, Lit, Referent, Unbound

type Position = Annotated[Referent | Lit | Held | Kinded | Unbound, Discriminator("occupies")]

type ReferentOrUnbound = Annotated[Referent | Unbound, Discriminator("occupies")]
type ReferentOrLiteral = Annotated[Referent | Lit, Discriminator("occupies")]
type ReferentOrLiteralOrUnbound = Annotated[Referent | Lit | Unbound, Discriminator("occupies")]
type ReferentOrStatement = Annotated[Referent | Held, Discriminator("occupies")]
type KindOrReferent = Annotated[Kinded | Referent, Discriminator("occupies")]


class Held(BaseModel):
    """A statement in a position. Holding one is what makes a statement second-order."""

    model_config = SEALED

    occupies: Literal["statement"] = "statement"
    statement: Statement


class Entity(BaseModel):
    """Asserts that a referent persists. Refuses to say what class it belongs to."""

    model_config = SEALED

    kind: Literal[OntokKind.ENTITY] = OntokKind.ENTITY
    subject: Referent
    predicate: Referent
    value: ReferentOrUnbound


class Event(BaseModel):
    """Asserts an occurrence. Refuses to say what obtains across an interval."""

    model_config = SEALED

    kind: Literal[OntokKind.EVENT] = OntokKind.EVENT
    subject: Referent
    predicate: Referent
    value: ReferentOrLiteralOrUnbound


class State(BaseModel):
    """Asserts a condition. Refuses to carry when it obtains, or whether it still does."""

    model_config = SEALED

    kind: Literal[OntokKind.STATE] = OntokKind.STATE
    subject: Referent
    predicate: Referent
    value: ReferentOrLiteral


class Role(BaseModel):
    """Asserts a capacity. One referent holds several capacities and remains one referent."""

    model_config = SEALED

    kind: Literal[OntokKind.ROLE] = OntokKind.ROLE
    subject: Referent
    predicate: Referent
    value: Referent


class Relation(BaseModel):
    """Connects two things, or two statements. Refuses to carry when the connection began."""

    model_config = SEALED

    kind: Literal[OntokKind.RELATION] = OntokKind.RELATION
    subject: ReferentOrStatement
    predicate: Referent
    value: ReferentOrStatement


class Claim(BaseModel):
    """Someone put the subject forward. Grounds it, and refuses to settle it."""

    model_config = SEALED

    kind: Literal[OntokKind.CLAIM] = OntokKind.CLAIM
    subject: Held
    predicate: Referent
    value: Referent


class Evidence(BaseModel):
    """An artifact bears the subject. Refuses to be what it cites."""

    model_config = SEALED

    kind: Literal[OntokKind.EVIDENCE] = OntokKind.EVIDENCE
    subject: Held
    predicate: Referent
    value: Referent


class Derivation(BaseModel):
    """The subject follows from a rule. Refuses to assert that the subject currently holds."""

    model_config = SEALED

    kind: Literal[OntokKind.DERIVATION] = OntokKind.DERIVATION
    subject: Held
    predicate: Referent
    value: Held


class Invalidation(BaseModel):
    """Someone released the subject. The released statement remains, and remains reachable."""

    model_config = SEALED

    kind: Literal[OntokKind.INVALIDATION] = OntokKind.INVALIDATION
    subject: Held
    predicate: Referent
    value: Referent


class Rule(BaseModel):
    """Premises conclude a statement. Names no predicate belonging to any domain."""

    model_config = SEALED

    kind: Literal[OntokKind.RULE] = OntokKind.RULE
    subject: Held
    predicate: Referent
    value: Held


class Context(BaseModel):
    """Bounds where or when the subject is put forward. Refuses to rank scopes."""

    model_config = SEALED

    kind: Literal[OntokKind.CONTEXT] = OntokKind.CONTEXT
    subject: Held
    predicate: Referent
    value: ReferentOrLiteral


class Concept(BaseModel):
    """Classifies a referent, reaching a kind directly or through another concept.

    The only kind whose value position holds a kind, and the only place a domain meets this model.
    `cust_no` is a Customer, and Customer is an entity: two of these, and the column is transcribed.
    """

    model_config = SEALED

    kind: Literal[OntokKind.CONCEPT] = OntokKind.CONCEPT
    subject: Referent
    predicate: Referent
    value: KindOrReferent


type Statement = Annotated[
    Entity
    | Event
    | State
    | Role
    | Relation
    | Claim
    | Evidence
    | Derivation
    | Invalidation
    | Rule
    | Context
    | Concept,
    Discriminator("kind"),
]

StatementConstructor: TypeAdapter[Statement] = TypeAdapter(Statement)
