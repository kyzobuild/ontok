from enum import StrEnum
from typing import Annotated, Literal, Self

from pydantic import BaseModel, ConfigDict, Field, RootModel, model_validator

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


class Contraries(RootModel[frozenset[Position]], frozen=True):
    """The positions a State excludes."""

    root: frozenset[Position] = Field(min_length=1)


class Rank(RootModel[int], frozen=True):
    """How high a position sits on a graded standing, lowest at zero."""

    root: int = Field(ge=0)


class State(Node):
    """Where a Node stands among the recognized positions of one standing."""


class Plain(State):
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

    @property
    def contraries(self) -> Contraries:
        """The positions this State excludes."""

        return Contraries(self.standing.root - {self.at})


class Graded(State):
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

    @property
    def contraries(self) -> Contraries:
        """The positions this State excludes."""

        return Contraries(frozenset(self.standing.root) - {self.at})

    @property
    def rank(self) -> Rank:
        """How high this position sits on its standing, lowest at zero."""

        return Rank(self.standing.root.index(self.at))


StateForms = Annotated[Plain | Graded, Field(discriminator="kind")]


class OutrankingKind(StrEnum):
    """How two Graded States sit relative to one standing."""

    OUTRANKS = "outranks"
    MATCHES = "matches"
    OUTRANKED = "outranked"
    INCOMPARABLE = "incomparable"


class Outranks(BaseModel):
    """This State sits higher than the other on one standing."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    kind: Literal[OutrankingKind.OUTRANKS] = OutrankingKind.OUTRANKS
    subject: Graded
    other: Graded


class Matches(BaseModel):
    """This State sits at the same place as the other on one standing."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    kind: Literal[OutrankingKind.MATCHES] = OutrankingKind.MATCHES
    subject: Graded
    other: Graded


class Outranked(BaseModel):
    """This State sits lower than the other on one standing."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    kind: Literal[OutrankingKind.OUTRANKED] = OutrankingKind.OUTRANKED
    subject: Graded
    other: Graded


class Incomparable(BaseModel):
    """The States do not share a standing."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    kind: Literal[OutrankingKind.INCOMPARABLE] = OutrankingKind.INCOMPARABLE
    subject: Graded
    other: Graded


OutrankingRelation = Annotated[
    Outranks | Matches | Outranked | Incomparable,
    Field(discriminator="kind"),
]


class Outranking(BaseModel):
    """Whether one Graded State sits higher than another."""

    model_config = ConfigDict(frozen=True, extra="forbid")
    subject: Graded
    other: Graded

    @property
    def answer(self) -> OutrankingRelation:
        """How the subject sits relative to the other."""

        return next(
            (
                {
                    (True, False): Outranks(subject=self.subject, other=self.other),
                    (False, True): Outranked(subject=self.subject, other=self.other),
                    (False, False): Matches(subject=self.subject, other=self.other),
                }[
                    self.subject.rank.root > self.other.rank.root,
                    self.subject.rank.root < self.other.rank.root,
                ]
                for shared in (self.subject.standing == self.other.standing,)
                if shared
            ),
            Incomparable(subject=self.subject, other=self.other),
        )
