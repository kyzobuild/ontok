from datetime import UTC, datetime

from pytest import fail

from ontok.core import Instant, NodeId, Timestamp
from ontok.ex import (
    LeftCompletion,
    LeftCompletionArrival,
    LeftOutcome,
    RightAfterLeftArrival,
    RightCompletion,
    RightOutcome,
)
from ontok.ex.execution import BeginningCompletedExecution


def test_second_branch_completion_constructs_the_exact_join(
    branches: BeginningCompletedExecution,
) -> None:
    left = LeftCompletion(
        id=NodeId("01900000-0000-7000-8000-000000000010"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 2, tzinfo=UTC))),
        activation=branches.left,
        outcome=LeftOutcome(id=NodeId("01900000-0000-7000-8000-000000000011")),
    )
    waiting = LeftCompletionArrival(completion=left).state
    right = RightCompletion(
        id=NodeId("01900000-0000-7000-8000-000000000012"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 3, tzinfo=UTC))),
        activation=waiting.right,
        outcome=RightOutcome(id=NodeId("01900000-0000-7000-8000-000000000013")),
    )
    joined = RightAfterLeftArrival(waiting=waiting, completion=right).state

    if joined.activation.prerequisite.left is not left:
        fail("The join lost its exact LeftCompletion.")
    if joined.activation.prerequisite.right is not right:
        fail("The join lost its exact RightCompletion.")
