from datetime import UTC, datetime

from pytest import fixture

from ontok.core import Instant, NodeId, Timestamp
from ontok.ex import (
    ActivationIdentities,
    BeginningCompletion,
    BeginningCompletionArrival,
    BeginningOutcome,
    Execution,
    ExecutionRequest,
    Program,
    ProgramNodes,
)
from ontok.ex.execution import BeginningCompletedExecution


@fixture
def execution_request() -> ExecutionRequest:
    return ExecutionRequest(
        id=NodeId("01900000-0000-7000-8000-000000000009"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, tzinfo=UTC))),
        program=Program(
            id=NodeId("01900000-0000-7000-8000-000000000001"),
            nodes=ProgramNodes(
                role=NodeId("01900000-0000-7000-8000-000000000002"),
                goal=NodeId("01900000-0000-7000-8000-000000000003"),
                action=NodeId("01900000-0000-7000-8000-000000000004"),
                beginning_work=NodeId("01900000-0000-7000-8000-000000000005"),
                left_work=NodeId("01900000-0000-7000-8000-000000000006"),
                right_work=NodeId("01900000-0000-7000-8000-000000000007"),
                joined_work=NodeId("01900000-0000-7000-8000-000000000008"),
            ),
        ),
        activations=ActivationIdentities(
            beginning=NodeId("01900000-0000-7000-8000-00000000000a"),
            left=NodeId("01900000-0000-7000-8000-00000000000b"),
            right=NodeId("01900000-0000-7000-8000-00000000000c"),
            joined=NodeId("01900000-0000-7000-8000-00000000000d"),
        ),
    )


@fixture
def beginning_completion(execution_request: ExecutionRequest) -> BeginningCompletion:
    return BeginningCompletion(
        id=NodeId("01900000-0000-7000-8000-00000000000e"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 18, 0, 1, tzinfo=UTC))),
        activation=Execution(request=execution_request).activation,
        outcome=BeginningOutcome(
            id=NodeId("01900000-0000-7000-8000-00000000000f")
        ),
    )


@fixture
def branches(beginning_completion: BeginningCompletion) -> BeginningCompletedExecution:
    return BeginningCompletionArrival(completion=beginning_completion).state
