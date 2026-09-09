from pydantic import Field

from ontok.core.action import Action
from ontok.core.context import Context
from ontok.core.goal import Goal
from ontok.core.role import Role
from ontok.core.structure import Node


class Rule(Node):
    """A constraint."""

    context: Context = Field(description="The situation this constraint is in.")
    role: Role = Field(description="The office this constraint is about.")
    goal: Goal = Field(description="The end this constraint is about.")
    doing: Action = Field(description="The doing this constraint is about.")
