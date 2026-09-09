from pydantic import Field, RootModel

from ontok.core.structure import Connection, Node


class RelationId(RootModel[str], frozen=True):
    """A canonical UUIDv7 identifier that distinguishes a Relation."""

    root: str = Field(
        pattern=r"^[0-9a-f]{8}-[0-9a-f]{4}-7[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    )


class Relation[SourceT: Node, TargetT: Node](Connection[SourceT, TargetT]):
    """An identifiable domain association from one Node to another."""

    id: RelationId = Field(description="The identifier that distinguishes this Relation.")
