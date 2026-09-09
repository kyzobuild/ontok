from pydantic import Field

from ontok.core.structure import Node
from ontok.core.time import TemporalExtent


class Event(Node):
    """An occurrence."""

    occurred: TemporalExtent = Field(description="When this occurred.")
