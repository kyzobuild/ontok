from functools import cached_property

from pydantic import Field, RootModel

from ontok.core.entity import Entity
from ontok.core.relation import Relation
from ontok.core.work import Work


class PlannedWork(RootModel[tuple[Work, ...]], frozen=True):
    """The Work declared for one execution."""

    root: tuple[Work, ...] = Field(min_length=1)


class Dependency(Relation[Work, Work]):
    """One Work whose completion enables another Work."""


class Dependencies(RootModel[tuple[Dependency, ...]], frozen=True):
    """The dependency graph of one execution."""


class TerminalWork(RootModel[tuple[Work, ...]], frozen=True):
    """The Work with no dependent Work."""


class ExecutionPlan(Entity):
    """The Work and dependencies declared for one execution."""

    work: PlannedWork
    dependency: Dependencies

    @cached_property
    def terminal(self) -> TerminalWork:
        """Work that enables no other Work in this plan."""
        return TerminalWork(
            tuple(
                work
                for work in self.work.root
                if all(dependency.source != work for dependency in self.dependency.root)
            )
        )
