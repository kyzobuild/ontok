from pydantic import Field, RootModel

from ontok.core.structure import Connection
from ontok.core.type import TypeId


class RelationId(RootModel[str], frozen=True):
    """A canonical UUIDv7 identifier that distinguishes a Relation."""

    root: str = Field(
        pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )


class Relation(Connection):
    """An identifiable domain association from one Node to another."""

    id: RelationId = Field(description="The identifier that distinguishes this Relation.")
    relation_type: TypeId = Field(
        description="The declared organizational type of this Relation."
    )
