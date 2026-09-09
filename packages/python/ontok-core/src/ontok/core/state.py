from enum import StrEnum
from functools import cached_property
from typing import Annotated, Literal, Self

from pydantic import Field, RootModel, model_validator

from ontok.core.structure import Node


class Position(RootModel[str], frozen=True):
    """One recognized position within a standing."""

    root: str = Field(pattern=r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")


class StandingKind(StrEnum):
    """The exhaustive forms a standing takes."""

    PLAIN = "plain"
    GRADED = "graded"


class PlainStanding(RootModel[frozenset[Position]], frozen=True):
    """The unordered positions of one standing, each excluding the others."""

    root: frozenset[Position] = Field(min_length=2)


class GradedStanding(RootModel[tuple[Position, ...]], frozen=True):
    """The positions of one standing in order, lowest first, each excluding the others."""

    root: tuple[Position, ...] = Field(min_length=2)

    @model_validator(mode="after")
    def positions_are_distinct(self) -> Self:
        """A standing names each position once."""

        if len(set(self.root)) != len(self.root):
            msg = "A standing names each of its positions once."
            raise ValueError(msg)
        return self


class Plain(Node):
    """The position a Node holds among unordered positions that exclude one another."""

    kind: Literal[StandingKind.PLAIN] = StandingKind.PLAIN
    standing: PlainStanding = Field(description="The positions this State stands among.")
    at: Position = Field(description="The position this State stands at.")

    @model_validator(mode="after")
    def stands_at_a_position_of_its_standing(self) -> Self:
        """A State stands at one of its standing's positions."""

        if self.at not in self.standing.root:
            msg = "A State stands at one of its standing's positions."
            raise ValueError(msg)
        return self

    @cached_property
    def contraries(self) -> frozenset[Position]:
        """The positions this State excludes."""

        return self.standing.root - {self.at}


class Graded(Node):
    """The position a Node holds on an ordered standing."""

    kind: Literal[StandingKind.GRADED] = StandingKind.GRADED
    standing: GradedStanding = Field(description="The ordered positions this State stands among.")
    at: Position = Field(description="The position this State stands at.")

    @model_validator(mode="after")
    def stands_at_a_position_of_its_standing(self) -> Self:
        """A State stands at one of its standing's positions."""

        if self.at not in self.standing.root:
            msg = "A State stands at one of its standing's positions."
            raise ValueError(msg)
        return self

    @cached_property
    def contraries(self) -> frozenset[Position]:
        """The positions this State excludes."""

        return frozenset(self.standing.root) - {self.at}

    @cached_property
    def rank(self) -> int:
        """How high this position sits on its standing, lowest at zero."""

        return self.standing.root.index(self.at)

    def outranks(self, other: "Graded") -> bool:
        """Whether this State sits higher than another State of the same standing."""

        if self.standing != other.standing:
            msg = "Only States of one standing compare."
            raise ValueError(msg)
        return self.rank > other.rank


State = Annotated[Plain | Graded, Field(discriminator="kind")]
