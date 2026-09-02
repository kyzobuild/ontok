from pydantic import Field

from ontok.core.structure import Node
from ontok.core.type import TypeId


class Entity(Node):
    """A particular thing whose identity persists as its conditions and associations change."""

    entity_type: TypeId = Field(description="The declared organizational type of this Entity.")
