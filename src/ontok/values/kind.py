"""The twelve kinds, and the three categories.

A kind is a way a statement can function. The world holds unbounded kinds of thing; there are only
so many ways a statement can function. Declaration order below is the order over kinds wherever an
order over kinds is required.
"""

from collections.abc import Mapping
from enum import StrEnum

from pydantic import RootModel


class Category(StrEnum):
    """What decides a category is which occupancies a statement's positions hold.

    Ordered kind before statement: a kind in any position decides reflexive, a statement with no
    kind decides second-order, and everything else is first-order.
    """

    FIRST_ORDER = "first-order"
    SECOND_ORDER = "second-order"
    REFLEXIVE = "reflexive"


class OntokKind(StrEnum):
    """The twelve. Closed here and extended by nobody."""

    ENTITY = "entity"
    EVENT = "event"
    STATE = "state"
    ROLE = "role"
    RELATION = "relation"
    CLAIM = "claim"
    EVIDENCE = "evidence"
    DERIVATION = "derivation"
    INVALIDATION = "invalidation"
    RULE = "rule"
    CONTEXT = "context"
    CONCEPT = "concept"


CATEGORY_OF: Mapping[OntokKind, Category] = {
    OntokKind.ENTITY: Category.FIRST_ORDER,
    OntokKind.EVENT: Category.FIRST_ORDER,
    OntokKind.STATE: Category.FIRST_ORDER,
    OntokKind.ROLE: Category.FIRST_ORDER,
    OntokKind.RELATION: Category.FIRST_ORDER,
    OntokKind.CLAIM: Category.SECOND_ORDER,
    OntokKind.EVIDENCE: Category.SECOND_ORDER,
    OntokKind.DERIVATION: Category.SECOND_ORDER,
    OntokKind.INVALIDATION: Category.SECOND_ORDER,
    OntokKind.RULE: Category.SECOND_ORDER,
    OntokKind.CONTEXT: Category.SECOND_ORDER,
    OntokKind.CONCEPT: Category.REFLEXIVE,
}

RANK_OF: Mapping[OntokKind, int] = {kind: rank for rank, kind in enumerate(OntokKind)}


class Kind(RootModel[OntokKind], frozen=True):
    """One of the twelve, as a value a position can hold."""

    root: OntokKind

    @property
    def category(self) -> Category:
        return CATEGORY_OF[self.root]

    @property
    def rank(self) -> int:
        return RANK_OF[self.root]
