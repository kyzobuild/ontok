from datetime import UTC, datetime

from pytest import fail

from ontok.core import (
    Action,
    Entity,
    Event,
    Goal,
    Instant,
    NodeId,
    RelationId,
    Role,
    Timestamp,
    Work,
)
from ontok.ex import (
    Activation,
    Completion,
    Dependencies,
    Dependency,
    ExecutionOrigin,
    ExecutionPlan,
    ExecutionProgression,
    ExecutionStatusKind,
    PlannedWork,
    TriggerEvents,
)


class ProgramRole(Role):
    """The office through which the example program acts."""


class ProgramGoal(Goal):
    """The end pursued by the example program."""


class ProgramAction(Action):
    """One declared doing in the example program."""


class ProgramWork(Work):
    """One persistent undertaking in the example program."""


class ProgramTrigger(Event):
    """An occurrence that starts the example program."""


class ProgramOutcome(Entity):
    """What came of performed example Work."""


def test_sequence_progresses_only_in_dependency_order() -> None:
    role = ProgramRole(id=NodeId("01900000-0000-7000-8000-000000000001"))
    goal = ProgramGoal(id=NodeId("01900000-0000-7000-8000-000000000002"))
    first = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000003"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000004"),
            role=role,
            goal=goal,
        ),
    )
    second = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000005"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000006"),
            role=role,
            goal=goal,
        ),
    )
    third = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000007"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000008"),
            role=role,
            goal=goal,
        ),
    )
    trigger = ProgramTrigger(
        id=NodeId("01900000-0000-7000-8000-000000000009"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 0, tzinfo=UTC))),
    )
    origin = ExecutionOrigin(
        id=NodeId("01900000-0000-7000-8000-00000000000a"),
        plan=ExecutionPlan(
            id=NodeId("01900000-0000-7000-8000-00000000000b"),
            work=PlannedWork((first, second, third)),
            dependency=Dependencies(
                (
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000000c"),
                        source=first,
                        target=second,
                    ),
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000000d"),
                        source=second,
                        target=third,
                    ),
                )
            ),
        ),
        trigger=trigger,
    )
    premature_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000014"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 0, 1, tzinfo=UTC))),
        activation=Activation(work=third, trigger=TriggerEvents((trigger,))),
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000015")),
    )
    premature = ExecutionProgression(
        id=origin.id,
        prior=origin,
        completion=premature_completion,
    )
    first_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-00000000000e"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 0, 1, tzinfo=UTC))),
        activation=origin.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-00000000000f")),
    )
    after_first = ExecutionProgression(
        id=origin.id,
        prior=premature,
        completion=first_completion,
    )
    second_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000010"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 0, 2, tzinfo=UTC))),
        activation=after_first.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000011")),
    )
    after_second = ExecutionProgression(
        id=origin.id,
        prior=after_first,
        completion=second_completion,
    )
    third_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000012"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 0, 3, tzinfo=UTC))),
        activation=after_second.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000013")),
    )
    finished = ExecutionProgression(
        id=origin.id,
        prior=after_second,
        completion=third_completion,
    )

    if tuple(activation.work for activation in origin.enabled.root) != (first,):
        fail("The sequence origin did not enable only its first Work.")
    if premature.completions.root:
        fail("Completion of Work that was never activated entered the execution.")
    if tuple(activation.work for activation in after_first.enabled.root) != (second,):
        fail("The first Completion did not enable only the second Work.")
    if tuple(activation.work for activation in after_second.enabled.root) != (third,):
        fail("The second Completion did not enable only the third Work.")
    if finished.status.kind is not ExecutionStatusKind.FINISHED:
        fail("The sequence did not finish after its terminal Work completed.")


def test_fan_out_enables_every_dependent_work_once() -> None:
    role = ProgramRole(id=NodeId("01900000-0000-7000-8000-000000000021"))
    goal = ProgramGoal(id=NodeId("01900000-0000-7000-8000-000000000022"))
    source = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000023"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000024"),
            role=role,
            goal=goal,
        ),
    )
    left = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000025"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000026"),
            role=role,
            goal=goal,
        ),
    )
    right = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000027"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000028"),
            role=role,
            goal=goal,
        ),
    )
    trigger = ProgramTrigger(
        id=NodeId("01900000-0000-7000-8000-000000000029"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 1, tzinfo=UTC))),
    )
    origin = ExecutionOrigin(
        id=NodeId("01900000-0000-7000-8000-00000000002a"),
        plan=ExecutionPlan(
            id=NodeId("01900000-0000-7000-8000-00000000002b"),
            work=PlannedWork((source, left, right)),
            dependency=Dependencies(
                (
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000002c"),
                        source=source,
                        target=left,
                    ),
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000002d"),
                        source=source,
                        target=right,
                    ),
                )
            ),
        ),
        trigger=trigger,
    )
    source_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-00000000002e"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 1, 1, tzinfo=UTC))),
        activation=origin.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-00000000002f")),
    )
    fan_out = ExecutionProgression(
        id=origin.id,
        prior=origin,
        completion=source_completion,
    )
    retried = ExecutionProgression(
        id=origin.id,
        prior=fan_out,
        completion=source_completion,
    )
    left_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000030"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 1, 2, tzinfo=UTC))),
        activation=fan_out.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000031")),
    )
    after_left = ExecutionProgression(
        id=origin.id,
        prior=retried,
        completion=left_completion,
    )
    right_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000032"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 1, 3, tzinfo=UTC))),
        activation=fan_out.enabled.root[1],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000033")),
    )
    finished = ExecutionProgression(
        id=origin.id,
        prior=after_left,
        completion=right_completion,
    )

    if tuple(activation.work for activation in fan_out.enabled.root) != (left, right):
        fail("The source Completion did not enable both dependent Work.")
    if retried.enabled.root or retried.completions.root != (source_completion,):
        fail("A retried Completion changed the execution a second time.")
    if after_left.enabled.root:
        fail("An unrelated Completion enabled fan-out Work a second time.")
    if finished.status.kind is not ExecutionStatusKind.FINISHED:
        fail("The fan-out did not finish after both terminal Work completed.")


def test_join_waits_for_every_prerequisite_completion() -> None:
    role = ProgramRole(id=NodeId("01900000-0000-7000-8000-000000000041"))
    goal = ProgramGoal(id=NodeId("01900000-0000-7000-8000-000000000042"))
    left = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000043"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000044"),
            role=role,
            goal=goal,
        ),
    )
    right = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000045"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000046"),
            role=role,
            goal=goal,
        ),
    )
    joined = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000047"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000048"),
            role=role,
            goal=goal,
        ),
    )
    trigger = ProgramTrigger(
        id=NodeId("01900000-0000-7000-8000-000000000049"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 2, tzinfo=UTC))),
    )
    origin = ExecutionOrigin(
        id=NodeId("01900000-0000-7000-8000-00000000004a"),
        plan=ExecutionPlan(
            id=NodeId("01900000-0000-7000-8000-00000000004b"),
            work=PlannedWork((left, right, joined)),
            dependency=Dependencies(
                (
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000004c"),
                        source=left,
                        target=joined,
                    ),
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000004d"),
                        source=right,
                        target=joined,
                    ),
                )
            ),
        ),
        trigger=trigger,
    )
    left_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-00000000004e"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 2, 1, tzinfo=UTC))),
        activation=origin.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-00000000004f")),
    )
    waiting = ExecutionProgression(
        id=origin.id,
        prior=origin,
        completion=left_completion,
    )
    right_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000050"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 2, 2, tzinfo=UTC))),
        activation=origin.enabled.root[1],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000051")),
    )
    joined_execution = ExecutionProgression(
        id=origin.id,
        prior=waiting,
        completion=right_completion,
    )

    if waiting.enabled.root:
        fail("The join enabled before every prerequisite Work completed.")
    if tuple(activation.work for activation in joined_execution.enabled.root) != (joined,):
        fail("The join did not enable after every prerequisite Work completed.")
    if joined_execution.enabled.root[0].trigger.root != (
        trigger,
        left_completion,
        right_completion,
    ):
        fail("The joined Work does not carry its complete triggering history.")


def test_external_completion_releases_blocked_work() -> None:
    role = ProgramRole(id=NodeId("01900000-0000-7000-8000-000000000061"))
    goal = ProgramGoal(id=NodeId("01900000-0000-7000-8000-000000000062"))
    external = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000063"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000064"),
            role=role,
            goal=goal,
        ),
    )
    waiting = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000065"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000066"),
            role=role,
            goal=goal,
        ),
    )
    trigger = ProgramTrigger(
        id=NodeId("01900000-0000-7000-8000-000000000067"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 3, tzinfo=UTC))),
    )
    origin = ExecutionOrigin(
        id=NodeId("01900000-0000-7000-8000-000000000068"),
        plan=ExecutionPlan(
            id=NodeId("01900000-0000-7000-8000-000000000069"),
            work=PlannedWork((waiting,)),
            dependency=Dependencies(
                (
                    Dependency(
                        id=RelationId("01900000-0000-7000-8000-00000000006a"),
                        source=external,
                        target=waiting,
                    ),
                )
            ),
        ),
        trigger=trigger,
    )
    external_completion = Completion(
        id=NodeId("01900000-0000-7000-8000-00000000006b"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 3, 1, tzinfo=UTC))),
        activation=Activation(work=external, trigger=TriggerEvents((trigger,))),
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-00000000006c")),
    )
    released = ExecutionProgression(
        id=origin.id,
        prior=origin,
        completion=external_completion,
    )

    if origin.status.kind is not ExecutionStatusKind.BLOCKED:
        fail("Work awaiting an external Completion was not blocked.")
    if tuple(activation.work for activation in released.enabled.root) != (waiting,):
        fail("The external Completion did not release its dependent Work.")
    if released.status.kind is not ExecutionStatusKind.ACTIVE:
        fail("The released Work is not represented as active.")


def test_terminal_completion_finishes_execution() -> None:
    role = ProgramRole(id=NodeId("01900000-0000-7000-8000-000000000081"))
    goal = ProgramGoal(id=NodeId("01900000-0000-7000-8000-000000000082"))
    terminal = ProgramWork(
        id=NodeId("01900000-0000-7000-8000-000000000083"),
        action=ProgramAction(
            id=NodeId("01900000-0000-7000-8000-000000000084"),
            role=role,
            goal=goal,
        ),
    )
    trigger = ProgramTrigger(
        id=NodeId("01900000-0000-7000-8000-000000000085"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 4, tzinfo=UTC))),
    )
    origin = ExecutionOrigin(
        id=NodeId("01900000-0000-7000-8000-000000000086"),
        plan=ExecutionPlan(
            id=NodeId("01900000-0000-7000-8000-000000000087"),
            work=PlannedWork((terminal,)),
            dependency=Dependencies(()),
        ),
        trigger=trigger,
    )
    completion = Completion(
        id=NodeId("01900000-0000-7000-8000-000000000088"),
        occurred=Instant(at=Timestamp(datetime(2026, 9, 9, 17, 4, 1, tzinfo=UTC))),
        activation=origin.enabled.root[0],
        outcome=ProgramOutcome(id=NodeId("01900000-0000-7000-8000-000000000089")),
    )
    finished = ExecutionProgression(
        id=origin.id,
        prior=origin,
        completion=completion,
    )

    if origin.status.kind is not ExecutionStatusKind.ACTIVE:
        fail("Terminal Work was not active before its Completion.")
    if finished.enabled.root:
        fail("Terminal Completion enabled Work after execution finished.")
    if finished.status.kind is not ExecutionStatusKind.FINISHED:
        fail("Terminal Completion did not finish the execution.")
