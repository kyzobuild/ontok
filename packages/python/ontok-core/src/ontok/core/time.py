from datetime import timedelta

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, RootModel


class Timestamp(RootModel[AwareDatetime], frozen=True):
    """A timezone-qualified point on the timeline."""

    root: AwareDatetime


class PositiveDuration(RootModel[timedelta], frozen=True):
    """A strictly positive length of elapsed time."""

    root: timedelta = Field(gt=timedelta(0))


class Instant(BaseModel):
    """A temporal extent occupying one point on the timeline."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    at: Timestamp


class Interval(BaseModel):
    """A temporal extent beginning at one point and continuing for positive time."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    begins_at: Timestamp
    duration: PositiveDuration


TemporalExtent = Instant | Interval
