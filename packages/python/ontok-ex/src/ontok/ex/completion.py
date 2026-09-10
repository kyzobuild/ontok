from functools import cached_property

from pydantic import RootModel

from ontok.core.entity import Entity
from ontok.core.event import Event
from ontok.core.work import Work
from ontok.ex.activation import Activation


class Completion(Event):
    """The occurrence and outcome of performed Work."""

    activation: Activation
    outcome: Entity


class Completions(RootModel[tuple[Completion, ...]], frozen=True):
    """The completed Work of one execution."""

    root: tuple[Completion, ...]

    @cached_property
    def work(self) -> "CompletedWork":
        return CompletedWork(tuple(completion.activation.work for completion in self.root))


class CompletedWork(RootModel[tuple[Work, ...]], frozen=True):
    """The Work represented by Completions."""

    root: tuple[Work, ...]
