from enum import StrEnum
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, RootModel

from ontok.core.work import Work
from ontok.ex.completion import CompletedWork
from ontok.ex.plan import TerminalWork


class ExecutionStatusKind(StrEnum):
    """The present disposition of an execution."""

    ACTIVE = "active"
    BLOCKED = "blocked"
    FINISHED = "finished"


class PendingWork(RootModel[tuple[Work, ...]], frozen=True):
    """Activated Work without a Completion."""

    root: tuple[Work, ...] = Field(min_length=1)


class Finished(BaseModel):
    """Every terminal Work has completed."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStatusKind.FINISHED] = ExecutionStatusKind.FINISHED
    completed: CompletedWork
    terminal: TerminalWork


class Active(BaseModel):
    """Work is active and awaiting Completion."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStatusKind.ACTIVE] = ExecutionStatusKind.ACTIVE
    completed: CompletedWork
    terminal: TerminalWork
    pending: PendingWork


class Blocked(BaseModel):
    """No Work is active and terminal Work remains incomplete."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[ExecutionStatusKind.BLOCKED] = ExecutionStatusKind.BLOCKED
    completed: CompletedWork
    terminal: TerminalWork


ExecutionStatus = Annotated[Active | Blocked | Finished, Field(discriminator="kind")]
