from pydantic import Field

from ontok.core.action import Action
from ontok.core.context import Context
from ontok.core.structure import Node


class Rule(Node):
    """A constraint on declared work within a situation."""

    context: Context = Field(description="The situation this constraint is in.")
    doing: Action = Field(description="The doing this constraint is about.")
