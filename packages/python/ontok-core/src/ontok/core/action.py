from pydantic import Field

from ontok.core.entity import Entity
from ontok.core.event import Event
from ontok.core.goal import Goal
from ontok.core.role import Role
from ontok.core.structure import Node


class Action(Node):
    """A doing."""

    role: Role = Field(description="The office through which this doing is taken.")
    goal: Goal = Field(description="The end this doing is toward.")
    result: Entity = Field(description="What came of the doing.")
    event: Event = Field(description="The occurrence of this doing.")
