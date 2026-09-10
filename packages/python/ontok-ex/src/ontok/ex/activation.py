from functools import cached_property

from pydantic import BaseModel, ConfigDict, Field, RootModel

from ontok.core.event import Event
from ontok.core.work import Work


class TriggerEvents(RootModel[tuple[Event, ...]], frozen=True):
    """The occurrences enabling one Work."""

    root: tuple[Event, ...] = Field(min_length=1)


class Activation(BaseModel):
    """Work enabled by its triggering occurrences."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    work: Work
    trigger: TriggerEvents


class Activations(RootModel[tuple[Activation, ...]], frozen=True):
    """A sequence of Work enablements."""

    root: tuple[Activation, ...]

    @cached_property
    def work(self) -> "ActivatedWork":
        """The Work carried by these Activations."""
        return ActivatedWork(tuple(activation.work for activation in self.root))


class ActivatedWork(RootModel[tuple[Work, ...]], frozen=True):
    """The Work represented by Activations."""

    root: tuple[Work, ...]
