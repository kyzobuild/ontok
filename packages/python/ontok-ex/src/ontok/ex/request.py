from pydantic import BaseModel, ConfigDict

from ontok.core import Event, NodeId
from ontok.ex.program import Program


class ActivationIdentities(BaseModel):
    """The identities reserved for one execution's Activations."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    beginning: NodeId
    left: NodeId
    right: NodeId
    joined: NodeId


class ExecutionRequest(Event):
    """An occurrence requesting execution of one declared Program."""

    program: Program
    activations: ActivationIdentities
