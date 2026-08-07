"""What a position holds, apart from a statement.

A position holds a referent, a literal, a statement, a kind, or nothing. Four of the five are here.
The fifth is a statement, and it lives beside the kinds it composes because it is the recursion.

ONTOK never names a referent and never describes one, so a referent is an opaque token here and
whether two referents are one referent is settled outside this model. ONTOK states no vocabulary of
literals and admits no division of them into sorts, so a literal is opaque for the same reason: the
value space belongs to another model, and importing one would make ONTOK privilege a substrate.
"""

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, RootModel, StringConstraints

from ontok.values.kind import Kind

SEALED = ConfigDict(frozen=True, extra="forbid")


class Token(RootModel[str], frozen=True):
    """An opaque name. Open: any non-empty text, to which this model assigns no meaning."""

    root: Annotated[str, StringConstraints(min_length=1)]


class Referent(BaseModel):
    """A thing. Its identity is asserted elsewhere; a value position holding one is an edge."""

    model_config = SEALED

    occupies: Literal["referent"] = "referent"
    name: Token


class Lit(BaseModel):
    """A value, identical to itself in every set of statements with no correspondence asserted."""

    model_config = SEALED

    occupies: Literal["literal"] = "literal"
    value: Token


class Kinded(BaseModel):
    """One of the twelve. Only a concept holds one."""

    model_config = SEALED

    occupies: Literal["kind"] = "kind"
    kind: Kind


class Unbound(BaseModel):
    """Nothing. A rule carries these and a derivation carries none."""

    model_config = SEALED

    occupies: Literal["unbound"] = "unbound"
