from enum import StrEnum
from functools import cached_property
from typing import Annotated, Literal

from pydantic import Field

from ontok.core.entity import Entity
from ontok.core.event import Event
from ontok.ex.activation import ActivatedWork, Activation, Activations, TriggerEvents
from ontok.ex.completion import CompletedWork, Completion, Completions
from ontok.ex.plan import ExecutionPlan
from ontok.ex.status import (
    Active,
    Blocked,
    ExecutionStatus,
    Finished,
    PendingWork,
)


class ExecutionKind(StrEnum):
    """The form of an execution's constructed history."""

    ORIGIN = "origin"
    PROGRESSION = "progression"


class ExecutionOrigin(Entity):
    """An execution constructed from its triggering occurrence."""

    kind: Literal[ExecutionKind.ORIGIN] = ExecutionKind.ORIGIN
    plan: ExecutionPlan
    trigger: Event

    @cached_property
    def completions(self) -> Completions:
        """No Work has completed at the execution's origin."""
        return Completions(())

    @cached_property
    def completed(self) -> CompletedWork:
        """No Work has completed at the execution's origin."""
        return self.completions.work

    @cached_property
    def enabled(self) -> Activations:
        """Work without prerequisites, enabled by the triggering occurrence."""
        return Activations(
            tuple(
                Activation(work=work, trigger=TriggerEvents((self.trigger,)))
                for work in self.plan.work.root
                if all(dependency.target != work for dependency in self.plan.dependency.root)
            )
        )

    @cached_property
    def activations(self) -> Activations:
        """Every Activation constructed for this execution."""
        return self.enabled

    @cached_property
    def activated(self) -> ActivatedWork:
        """Every Work represented by this execution's Activations."""
        return self.activations.work

    @cached_property
    def status(self) -> ExecutionStatus:
        """Whether this execution is active, blocked, or finished."""
        return next(
            (
                Finished(completed=self.completed, terminal=terminal)
                for terminal in (self.plan.terminal,)
                if terminal.root
                if all(work in self.completed.root for work in terminal.root)
            ),
            next(
                (
                    Active(
                        completed=self.completed,
                        terminal=self.plan.terminal,
                        pending=PendingWork(pending),
                    )
                    for pending in (
                        tuple(
                            work
                            for work in self.activated.root
                            if work not in self.completed.root
                        ),
                    )
                    if pending
                ),
                Blocked(completed=self.completed, terminal=self.plan.terminal),
            ),
        )


class ExecutionProgression(Entity):
    """An execution reconstructed by one Work Completion."""

    kind: Literal[ExecutionKind.PROGRESSION] = ExecutionKind.PROGRESSION
    prior: "Execution"
    completion: Completion

    @cached_property
    def plan(self) -> ExecutionPlan:
        """The plan established at this execution's origin."""
        return self.prior.plan

    @cached_property
    def trigger(self) -> Event:
        """The occurrence that established this execution."""
        return self.prior.trigger

    @cached_property
    def completions(self) -> Completions:
        """Every applicable, distinct Completion accepted by this execution."""
        return Completions(
            (
                *self.prior.completions.root,
                *(
                    self.completion
                    for _ in (0,)
                    if self.completion not in self.prior.completions.root
                    if self.completion.activation in self.prior.activations.root
                ),
                *(
                    self.completion
                    for _ in (0,)
                    if self.completion not in self.prior.completions.root
                    if self.completion.activation.work not in self.plan.work.root
                    if any(
                        dependency.source == self.completion.activation.work
                        for dependency in self.plan.dependency.root
                        if dependency.target in self.plan.work.root
                    )
                ),
            )
        )

    @cached_property
    def completed(self) -> CompletedWork:
        """Every Work represented by this execution's Completions."""
        return self.completions.work

    @cached_property
    def enabled(self) -> Activations:
        """Previously inactive Work enabled by this Completion."""
        return Activations(
            tuple(
                Activation(
                    work=work,
                    trigger=TriggerEvents(
                        (
                            self.trigger,
                            *(
                                completion
                                for completion in self.completions.root
                                if any(
                                    dependency.source == completion.activation.work
                                    for dependency in self.plan.dependency.root
                                    if dependency.target == work
                                )
                            ),
                        )
                    ),
                )
                for work in self.plan.work.root
                if work not in self.prior.activated.root
                if work not in self.completed.root
                if any(dependency.target == work for dependency in self.plan.dependency.root)
                if all(
                    dependency.source in self.completed.root
                    for dependency in self.plan.dependency.root
                    if dependency.target == work
                )
            )
        )

    @cached_property
    def activations(self) -> Activations:
        """Every Activation constructed across this execution's history."""
        return Activations((*self.prior.activations.root, *self.enabled.root))

    @cached_property
    def activated(self) -> ActivatedWork:
        """Every Work represented by this execution's Activations."""
        return self.activations.work

    @cached_property
    def status(self) -> ExecutionStatus:
        """Whether this execution is active, blocked, or finished."""
        return next(
            (
                Finished(completed=self.completed, terminal=terminal)
                for terminal in (self.plan.terminal,)
                if terminal.root
                if all(work in self.completed.root for work in terminal.root)
            ),
            next(
                (
                    Active(
                        completed=self.completed,
                        terminal=self.plan.terminal,
                        pending=PendingWork(pending),
                    )
                    for pending in (
                        tuple(
                            work
                            for work in self.activated.root
                            if work not in self.completed.root
                        ),
                    )
                    if pending
                ),
                Blocked(completed=self.completed, terminal=self.plan.terminal),
            ),
        )


Execution = Annotated[
    ExecutionOrigin | ExecutionProgression,
    Field(discriminator="kind"),
]
