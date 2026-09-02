from functools import cached_property
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel, computed_field

from ontok.core.relation import RelationId
from ontok.core.structure import Node
from ontok.core.time import NonNegativeDuration, TemporalExtent, Timestamp
from ontok.core.type import TypeId


class Memorialization(BaseModel):
    """The creation of a durable memorial by one organizational Node after an occurrence."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    memorializer: Node
    delay: NonNegativeDuration


class Event(Node):
    """A durable memorial of one organizational occurrence."""

    event_type: TypeId = Field(description="The declared organizational type of this Event.")
    memorialization: Memorialization = Field(
        description="The creation of this durable memorial."
    )
    occurred: TemporalExtent = Field(
        description="The complete temporal extent occupied by the occurrence."
    )

    @computed_field
    @cached_property
    def recorded_at(self) -> Timestamp:
        """The time derived from occurrence end and memorialization delay."""

        return Timestamp(self.occurred.ends_at.root + self.memorialization.delay.root)


class CausationTypeId(
    RootModel[Literal["urn:ontok:relation:causation"]],
    frozen=True,
):
    """The type identity carried by every Causation."""

    root: Literal["urn:ontok:relation:causation"] = "urn:ontok:relation:causation"


class Causation(BaseModel):
    """A Relation declaring that one Event caused another Event."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: RelationId
    relation_type: CausationTypeId = Field(default_factory=CausationTypeId)
    source: Event
    target: Event
