from pydantic import BaseModel, ConfigDict, Field

from ontok.core.identity import NodeId


class Node(BaseModel):
    """A distinct thing represented in the organizational graph."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    id: NodeId = Field(description="The identifier that distinguishes this Node.")


class Connection[SourceT: Node, TargetT: Node](BaseModel):
    """A typed link declaring how Nodes relate within the organizational graph."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    source: SourceT = Field(description="The Node from which the Connection originates.")
    target: TargetT = Field(description="The Node at which the Connection terminates.")
