from datetime import UTC, datetime

from pytest import fail

from ontok.core import Instant, NodeId, Timestamp
from ontok.ex import (
    ExecutionRequest,
    JoinedCompletion,
    JoinedCompletionArrival,
    JoinedOutcome,
    LeftCompletion,
    LeftCompletionArrival,
    LeftOutcome,
    RightAfterLeftArrival,
    RightCompletion,
    RightOutcome,
)
from ontok.ex.execution import BeginningCompletedExecution


def test_terminal_completion_preserves_the_complete_execution(
    execution_request: ExecutionRequest,
    branches: BeginningCompletedExecution,
) -> None:
    left = LeftCompletion(
        id=NodeId("01900000-0000-7000-8000-00000000001c"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 2, tzinfo=UTC))),
        activation=branches.left,
        outcome=LeftOutcome(id=NodeId("01900000-0000-7000-8000-00000000001d")),
    )
    waiting = LeftCompletionArrival(completion=left).state
    right = RightCompletion(
        id=NodeId("01900000-0000-7000-8000-00000000001e"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 3, tzinfo=UTC))),
        activation=waiting.right,
        outcome=RightOutcome(id=NodeId("01900000-0000-7000-8000-00000000001f")),
    )
    joined = RightAfterLeftArrival(waiting=waiting, completion=right).state
    completion = JoinedCompletion(
        id=NodeId("01900000-0000-7000-8000-000000000020"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 4, tzinfo=UTC))),
        activation=joined.activation,
        outcome=JoinedOutcome(id=NodeId("01900000-0000-7000-8000-000000000021")),
    )
    terminal = JoinedCompletionArrival(completion=completion).state

    if terminal.emission.completion is not completion:
        fail("The terminal execution did not emit its exact Completion.")
    if terminal.request is not execution_request:
        fail("The terminal execution lost its originating request.")
    if terminal.completion.activation.prerequisite.left is not left:
        fail("The terminal execution lost its left branch history.")
    if terminal.completion.activation.prerequisite.right is not right:
        fail("The terminal execution lost its right branch history.")
