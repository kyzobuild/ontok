from datetime import UTC, datetime

from pytest import fail

from ontok.core import Instant, NodeId, Timestamp
from ontok.ex import (
    LeftAfterRightArrival,
    LeftCompletion,
    LeftCompletionArrival,
    LeftOutcome,
    RightAfterLeftArrival,
    RightCompletion,
    RightCompletionArrival,
    RightOutcome,
)
from ontok.ex.execution import BeginningCompletedExecution


def test_either_branch_order_waits_then_resumes_the_join(
    branches: BeginningCompletedExecution,
) -> None:
    left = LeftCompletion(
        id=NodeId("01900000-0000-7000-8000-000000000014"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 2, tzinfo=UTC))),
        activation=branches.left,
        outcome=LeftOutcome(id=NodeId("01900000-0000-7000-8000-000000000015")),
    )
    waiting_for_right = LeftCompletionArrival(completion=left).state
    right = RightCompletion(
        id=NodeId("01900000-0000-7000-8000-000000000016"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 3, tzinfo=UTC))),
        activation=waiting_for_right.right,
        outcome=RightOutcome(id=NodeId("01900000-0000-7000-8000-000000000017")),
    )
    resumed_after_left = RightAfterLeftArrival(
        waiting=waiting_for_right,
        completion=right,
    ).state

    if waiting_for_right.emission.right != branches.right:
        fail("LeftCompletion did not preserve the outstanding RightActivation.")
    if resumed_after_left.activation.prerequisite.left is not left:
        fail("RightCompletion did not resume the join after LeftCompletion.")

    right_first = RightCompletion(
        id=NodeId("01900000-0000-7000-8000-000000000018"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 2, tzinfo=UTC))),
        activation=branches.right,
        outcome=RightOutcome(id=NodeId("01900000-0000-7000-8000-000000000019")),
    )
    waiting_for_left = RightCompletionArrival(completion=right_first).state
    left_second = LeftCompletion(
        id=NodeId("01900000-0000-7000-8000-00000000001a"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 3, tzinfo=UTC))),
        activation=waiting_for_left.left,
        outcome=LeftOutcome(id=NodeId("01900000-0000-7000-8000-00000000001b")),
    )
    resumed_after_right = LeftAfterRightArrival(
        waiting=waiting_for_left,
        completion=left_second,
    ).state

    if waiting_for_left.emission.left != branches.left:
        fail("RightCompletion did not preserve the outstanding LeftActivation.")
    if resumed_after_right.activation.prerequisite.right is not right_first:
        fail("LeftCompletion did not resume the join after RightCompletion.")
