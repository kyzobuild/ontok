from functools import cached_property

from pydantic import BaseModel, ConfigDict, Field, computed_field

from ontok.core.relation import Relation
from ontok.core.structure import Node
from ontok.core.time import NonNegativeDuration, TemporalExtent, Timestamp


class Memorialization(BaseModel):
    """The creation of a durable memorial by one organizational Node after an occurrence."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    memorializer: Node
    delay: NonNegativeDuration


class Event(Node):
    """A durable memorial of one organizational occurrence."""

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


class Causation(Relation[Event, Event]):
    """A Relation declaring that one Event caused another Event."""
