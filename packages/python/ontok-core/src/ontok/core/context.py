from pydantic import Field, RootModel

from ontok.core.state import State
from ontok.core.structure import Node


class States(RootModel[tuple[State, ...]], frozen=True):
    """The conditions that constitute a situation."""

    root: tuple[State, ...] = Field(min_length=1)


class Context(Node):
    """A situation."""

    state: States = Field(description="The conditions that hold in this situation.")
