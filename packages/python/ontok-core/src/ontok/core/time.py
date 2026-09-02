from datetime import timedelta
from enum import StrEnum
from functools import cached_property
from typing import Annotated, Literal

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class Timestamp(RootModel[AwareDatetime], frozen=True):
    """A timezone-qualified point on the timeline."""

    root: AwareDatetime


class PositiveDuration(RootModel[timedelta], frozen=True):
    """A strictly positive length of elapsed time."""

    root: timedelta = Field(gt=timedelta(0))


class NonNegativeDuration(RootModel[timedelta], frozen=True):
    """A length of elapsed time that cannot precede its origin."""

    root: timedelta = Field(ge=timedelta(0))


class TemporalExtentKind(StrEnum):
    """The exhaustive ways an occurrence can occupy time."""

    INSTANT = "instant"
    INTERVAL = "interval"


class Instant(BaseModel):
    """A temporal extent occupying one point on the timeline."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[TemporalExtentKind.INSTANT] = TemporalExtentKind.INSTANT
    at: Timestamp

    @property
    def ends_at(self) -> Timestamp:
        """The point occupied by this Instant."""

        return self.at


class Interval(BaseModel):
    """A temporal extent beginning at one point and continuing for positive time."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    kind: Literal[TemporalExtentKind.INTERVAL] = TemporalExtentKind.INTERVAL
    begins_at: Timestamp
    duration: PositiveDuration

    @cached_property
    def ends_at(self) -> Timestamp:
        """The point at which this Interval ends."""

        return Timestamp(self.begins_at.root + self.duration.root)


TemporalExtent = Annotated[Instant | Interval, Field(discriminator="kind")]
