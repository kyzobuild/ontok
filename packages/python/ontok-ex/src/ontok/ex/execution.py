from enum import StrEnum
from functools import cached_property
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, computed_field

from ontok.core import Entity, NodeId
from ontok.ex.activation import Activation
from ontok.ex.completion import Completion
from ontok.ex.program import BeginningWork, JoinedWork, LeftWork, RightWork
from ontok.ex.request import ExecutionRequest


class BeginningOutcome(Entity):
    """What came of BeginningWork."""


class LeftOutcome(Entity):
    """What came of LeftWork."""


class RightOutcome(Entity):
    """What came of RightWork."""


class JoinedOutcome(Entity):
    """What came of JoinedWork."""


class BeginningActivation(Activation):
    """BeginningWork enabled by an ExecutionRequest."""

    work: BeginningWork
    prerequisite: ExecutionRequest

    @computed_field
    @property
    def execution(self) -> NodeId:
        return self.prerequisite.id


class BeginningCompletion(Completion):
    """BeginningWork completed with its exact Activation and outcome."""

    activation: BeginningActivation
    outcome: BeginningOutcome


class LeftActivation(Activation):
    """LeftWork enabled by BeginningCompletion."""

    work: LeftWork
    prerequisite: BeginningCompletion

    @computed_field
    @property
    def execution(self) -> NodeId:
        return self.prerequisite.activation.execution


class LeftCompletion(Completion):
    """LeftWork completed with its exact Activation and outcome."""

    activation: LeftActivation
    outcome: LeftOutcome


class RightActivation(Activation):
    """RightWork enabled by BeginningCompletion."""

    work: RightWork
    prerequisite: BeginningCompletion

    @computed_field
    @property
    def execution(self) -> NodeId:
        return self.prerequisite.activation.execution


class RightCompletion(Completion):
    """RightWork completed with its exact Activation and outcome."""

    activation: RightActivation
    outcome: RightOutcome


class BranchesCompleted(BaseModel):
    """The exact complete prerequisite product for JoinedWork."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    left: LeftCompletion
    right: RightCompletion


class JoinedActivation(Activation):
    """JoinedWork enabled by both exact branch Completions."""

    work: JoinedWork
    prerequisite: BranchesCompleted

    @computed_field
    @property
    def execution(self) -> NodeId:
        return self.prerequisite.left.activation.execution


class JoinedCompletion(Completion):
    """JoinedWork completed with its exact Activation and outcome."""

    activation: JoinedActivation
    outcome: JoinedOutcome


class ExecutionEmissionKind(StrEnum):
    """The exact fact emitted by an execution construction."""

    BEGINNING_ACTIVATED = "beginning_activated"
    BRANCHES_ACTIVATED = "branches_activated"
    WAITING_FOR_RIGHT = "waiting_for_right"
    WAITING_FOR_LEFT = "waiting_for_left"
    JOINED_ACTIVATED = "joined_activated"
    EXECUTION_COMPLETED = "execution_completed"


class BeginningActivated(BaseModel):
    """The beginning Activation emitted for an ExecutionRequest."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionEmissionKind.BEGINNING_ACTIVATED] = (
        ExecutionEmissionKind.BEGINNING_ACTIVATED
    )
    activation: BeginningActivation


class BranchesActivated(BaseModel):
    """Both branch Activations emitted by BeginningCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionEmissionKind.BRANCHES_ACTIVATED] = (
        ExecutionEmissionKind.BRANCHES_ACTIVATED
    )
    left: LeftActivation
    right: RightActivation


class WaitingForRightCompletion(BaseModel):
    """LeftWork completed while RightWork remains active."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionEmissionKind.WAITING_FOR_RIGHT] = (
        ExecutionEmissionKind.WAITING_FOR_RIGHT
    )
    left: LeftCompletion
    right: RightActivation


class WaitingForLeftCompletion(BaseModel):
    """RightWork completed while LeftWork remains active."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionEmissionKind.WAITING_FOR_LEFT] = (
        ExecutionEmissionKind.WAITING_FOR_LEFT
    )
    right: RightCompletion
    left: LeftActivation


class JoinedActivated(BaseModel):
    """The joined Activation emitted by complete branch prerequisites."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionEmissionKind.JOINED_ACTIVATED] = (
        ExecutionEmissionKind.JOINED_ACTIVATED
    )
    activation: JoinedActivation


class ExecutionCompleted(BaseModel):
    """The terminal Completion emitted by a finished execution."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionEmissionKind.EXECUTION_COMPLETED] = (
        ExecutionEmissionKind.EXECUTION_COMPLETED
    )
    completion: JoinedCompletion


ExecutionEmission = Annotated[
    BeginningActivated
    | BranchesActivated
    | WaitingForRightCompletion
    | WaitingForLeftCompletion
    | JoinedActivated
    | ExecutionCompleted,
    Field(discriminator="kind"),
]


class ExecutionStateKind(StrEnum):
    """The exact lifecycle state constructed for an execution."""

    REQUESTED = "requested"
    BEGINNING_COMPLETED = "beginning_completed"
    WAITING_FOR_RIGHT = "waiting_for_right"
    WAITING_FOR_LEFT = "waiting_for_left"
    JOINED_AFTER_LEFT = "joined_after_left"
    JOINED_AFTER_RIGHT = "joined_after_right"
    TERMINAL = "terminal"


class Execution(BaseModel):
    """An execution constructed from its request."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.REQUESTED] = ExecutionStateKind.REQUESTED
    request: ExecutionRequest

    @cached_property
    def activation(self) -> BeginningActivation:
        return BeginningActivation(
            id=self.request.activations.beginning,
            occurred=self.request.occurred,
            work=self.request.program.beginning_work,
            prerequisite=self.request,
        )

    @cached_property
    def emission(self) -> BeginningActivated:
        return BeginningActivated(activation=self.activation)


class BeginningCompletedExecution(BaseModel):
    """An execution whose BeginningWork has completed."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.BEGINNING_COMPLETED] = (
        ExecutionStateKind.BEGINNING_COMPLETED
    )
    completion: BeginningCompletion

    @property
    def request(self) -> ExecutionRequest:
        return self.completion.activation.prerequisite

    @cached_property
    def left(self) -> LeftActivation:
        return LeftActivation(
            id=self.request.activations.left,
            occurred=self.completion.occurred,
            work=self.request.program.left_work,
            prerequisite=self.completion,
        )

    @cached_property
    def right(self) -> RightActivation:
        return RightActivation(
            id=self.request.activations.right,
            occurred=self.completion.occurred,
            work=self.request.program.right_work,
            prerequisite=self.completion,
        )

    @cached_property
    def emission(self) -> BranchesActivated:
        return BranchesActivated(left=self.left, right=self.right)


class WaitingForRight(BaseModel):
    """An execution with LeftWork complete and RightWork still active."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.WAITING_FOR_RIGHT] = ExecutionStateKind.WAITING_FOR_RIGHT
    left: LeftCompletion

    @property
    def beginning(self) -> BeginningCompletion:
        return self.left.activation.prerequisite

    @property
    def request(self) -> ExecutionRequest:
        return self.beginning.activation.prerequisite

    @cached_property
    def right(self) -> RightActivation:
        return RightActivation(
            id=self.request.activations.right,
            occurred=self.beginning.occurred,
            work=self.request.program.right_work,
            prerequisite=self.beginning,
        )

    @cached_property
    def emission(self) -> WaitingForRightCompletion:
        return WaitingForRightCompletion(left=self.left, right=self.right)


class WaitingForLeft(BaseModel):
    """An execution with RightWork complete and LeftWork still active."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.WAITING_FOR_LEFT] = ExecutionStateKind.WAITING_FOR_LEFT
    right: RightCompletion

    @property
    def beginning(self) -> BeginningCompletion:
        return self.right.activation.prerequisite

    @property
    def request(self) -> ExecutionRequest:
        return self.beginning.activation.prerequisite

    @cached_property
    def left(self) -> LeftActivation:
        return LeftActivation(
            id=self.request.activations.left,
            occurred=self.beginning.occurred,
            work=self.request.program.left_work,
            prerequisite=self.beginning,
        )

    @cached_property
    def emission(self) -> WaitingForLeftCompletion:
        return WaitingForLeftCompletion(right=self.right, left=self.left)


class JoinedAfterLeft(BaseModel):
    """An execution joined by RightCompletion after LeftCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.JOINED_AFTER_LEFT] = ExecutionStateKind.JOINED_AFTER_LEFT
    waiting: WaitingForRight
    right: RightCompletion

    @property
    def request(self) -> ExecutionRequest:
        return self.waiting.request

    @cached_property
    def prerequisite(self) -> BranchesCompleted:
        return BranchesCompleted(left=self.waiting.left, right=self.right)

    @cached_property
    def activation(self) -> JoinedActivation:
        return JoinedActivation(
            id=self.request.activations.joined,
            occurred=self.right.occurred,
            work=self.request.program.joined_work,
            prerequisite=self.prerequisite,
        )

    @cached_property
    def emission(self) -> JoinedActivated:
        return JoinedActivated(activation=self.activation)


class JoinedAfterRight(BaseModel):
    """An execution joined by LeftCompletion after RightCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.JOINED_AFTER_RIGHT] = ExecutionStateKind.JOINED_AFTER_RIGHT
    waiting: WaitingForLeft
    left: LeftCompletion

    @property
    def request(self) -> ExecutionRequest:
        return self.waiting.request

    @cached_property
    def prerequisite(self) -> BranchesCompleted:
        return BranchesCompleted(left=self.left, right=self.waiting.right)

    @cached_property
    def activation(self) -> JoinedActivation:
        return JoinedActivation(
            id=self.request.activations.joined,
            occurred=self.left.occurred,
            work=self.request.program.joined_work,
            prerequisite=self.prerequisite,
        )

    @cached_property
    def emission(self) -> JoinedActivated:
        return JoinedActivated(activation=self.activation)


class TerminalExecution(BaseModel):
    """An execution proven complete by JoinedCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStateKind.TERMINAL] = ExecutionStateKind.TERMINAL
    completion: JoinedCompletion

    @property
    def request(self) -> ExecutionRequest:
        return (
            self.completion.activation.prerequisite.left.activation.prerequisite.activation.prerequisite
        )

    @cached_property
    def emission(self) -> ExecutionCompleted:
        return ExecutionCompleted(completion=self.completion)


ExecutionState = Annotated[
    Execution
    | BeginningCompletedExecution
    | WaitingForRight
    | WaitingForLeft
    | JoinedAfterLeft
    | JoinedAfterRight
    | TerminalExecution,
    Field(discriminator="kind"),
]


class BeginningCompletionArrival(BaseModel):
    """BeginningCompletion constructing branch activation."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    completion: BeginningCompletion

    @cached_property
    def state(self) -> BeginningCompletedExecution:
        return BeginningCompletedExecution(completion=self.completion)

    @property
    def emission(self) -> BranchesActivated:
        return self.state.emission


class LeftCompletionArrival(BaseModel):
    """The first branch Completion when it is LeftCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    completion: LeftCompletion

    @cached_property
    def state(self) -> WaitingForRight:
        return WaitingForRight(left=self.completion)

    @property
    def emission(self) -> WaitingForRightCompletion:
        return self.state.emission


class RightCompletionArrival(BaseModel):
    """The first branch Completion when it is RightCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    completion: RightCompletion

    @cached_property
    def state(self) -> WaitingForLeft:
        return WaitingForLeft(right=self.completion)

    @property
    def emission(self) -> WaitingForLeftCompletion:
        return self.state.emission


class RightAfterLeftArrival(BaseModel):
    """RightCompletion constructing joined execution after LeftCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    waiting: WaitingForRight
    completion: RightCompletion

    @cached_property
    def state(self) -> JoinedAfterLeft:
        return JoinedAfterLeft(waiting=self.waiting, right=self.completion)

    @property
    def emission(self) -> JoinedActivated:
        return self.state.emission


class LeftAfterRightArrival(BaseModel):
    """LeftCompletion constructing joined execution after RightCompletion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    waiting: WaitingForLeft
    completion: LeftCompletion

    @cached_property
    def state(self) -> JoinedAfterRight:
        return JoinedAfterRight(waiting=self.waiting, left=self.completion)

    @property
    def emission(self) -> JoinedActivated:
        return self.state.emission


class JoinedCompletionArrival(BaseModel):
    """JoinedCompletion constructing terminal execution."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    completion: JoinedCompletion

    @cached_property
    def state(self) -> TerminalExecution:
        return TerminalExecution(completion=self.completion)

    @property
    def emission(self) -> ExecutionCompleted:
        return self.state.emission
