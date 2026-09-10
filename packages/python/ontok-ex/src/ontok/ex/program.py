from functools import cached_property

from pydantic import BaseModel, ConfigDict

from ontok.core import (
    Action,
    Goal,
    Node,
    NodeId,
    Role,
    Work,
)


class ProgramRole(Role):
    """The office through which the program acts."""


class ProgramGoal(Goal):
    """The end pursued by the program."""


class ProgramAction(Action):
    """The doing declared by the program."""


class BeginningWork(Work):
    """The Work that begins the program."""


class LeftWork(Work):
    """The Work on the left branch."""


class RightWork(Work):
    """The Work on the right branch."""


class JoinedWork(Work):
    """The Work requiring both branches."""


class ProgramNodes(BaseModel):
    """The identities of the exact Nodes declared by a Program."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    role: NodeId
    goal: NodeId
    action: NodeId
    beginning_work: NodeId
    left_work: NodeId
    right_work: NodeId
    joined_work: NodeId


class Program(Node):
    """The exact Work declaration executed by ontok-ex."""

    nodes: ProgramNodes

    @cached_property
    def role(self) -> ProgramRole:
        return ProgramRole(id=self.nodes.role)

    @cached_property
    def goal(self) -> ProgramGoal:
        return ProgramGoal(id=self.nodes.goal)

    @cached_property
    def action(self) -> ProgramAction:
        return ProgramAction(id=self.nodes.action, role=self.role, goal=self.goal)

    @cached_property
    def beginning_work(self) -> BeginningWork:
        return BeginningWork(id=self.nodes.beginning_work, action=self.action)

    @cached_property
    def left_work(self) -> LeftWork:
        return LeftWork(id=self.nodes.left_work, action=self.action)

    @cached_property
    def right_work(self) -> RightWork:
        return RightWork(id=self.nodes.right_work, action=self.action)

    @cached_property
    def joined_work(self) -> JoinedWork:
        return JoinedWork(id=self.nodes.joined_work, action=self.action)
