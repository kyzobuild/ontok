"""The Ontology Kernel.

A notation, not an ontology. It names what the statements in a system are already doing, and a
statement functions the same way whether it lives in a Fabric ontology, a KyzoDB record, or a
spreadsheet. Implementations stay local. Meaning becomes shared.
"""

from ontok.values.kind import CATEGORY_OF, RANK_OF, Category, Kind, OntokKind
from ontok.values.occupancy import Kinded, Lit, Referent, Token, Unbound
from ontok.values.statement import (
    Claim,
    Concept,
    Context,
    Derivation,
    Entity,
    Event,
    Evidence,
    Held,
    Invalidation,
    Position,
    Relation,
    Role,
    Rule,
    State,
    Statement,
    StatementConstructor,
)

__all__ = [
    "CATEGORY_OF",
    "RANK_OF",
    "Category",
    "Claim",
    "Concept",
    "Context",
    "Derivation",
    "Entity",
    "Event",
    "Evidence",
    "Held",
    "Invalidation",
    "Kind",
    "Kinded",
    "Lit",
    "OntokKind",
    "Position",
    "Referent",
    "Relation",
    "Role",
    "Rule",
    "State",
    "Statement",
    "StatementConstructor",
    "Token",
    "Unbound",
]
