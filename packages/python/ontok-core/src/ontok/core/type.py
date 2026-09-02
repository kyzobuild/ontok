from functools import cached_property

from pydantic import BaseModel, ConfigDict, Field, RootModel


class TypeId(RootModel[str], frozen=True):
    """The globally unique identity of a declared organizational type."""

    root: str = Field(
        pattern=r"^[a-z][a-z0-9+.-]*:[^\s]+$",
        description="A URI identifying one declared organizational type.",
    )


class SchemaVersion(RootModel[int], frozen=True):
    """The positive version of the schema defining a declared type."""

    root: int = Field(gt=0)


class VersionIncrement(RootModel[int], frozen=True):
    """A positive advance from one schema version to its successor."""

    root: int = Field(gt=0)


class SchemaSuccession(BaseModel):
    """The succession of one organizational type's schema by a later version."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    type_id: TypeId
    predecessor: SchemaVersion
    increment: VersionIncrement

    @cached_property
    def successor(self) -> SchemaVersion:
        """The schema version produced by this succession."""

        return SchemaVersion(self.predecessor.root + self.increment.root)
