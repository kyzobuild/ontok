---
type: Reference
description: How environment and deployment input constructs frozen typed configuration. Read when adding settings, environment variables, defaults, or secrets.
---

# Config

## Use

Use for values supplied by the deployment environment and required to construct runtime capabilities.

The package declaring this construct declares `pydantic-settings>=2,<3` beside its Pydantic dependency.

## Required Form

```python
class VenueConfig(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        extra="forbid",
        strict=True,
        validate_default=True,
        revalidate_instances="never",
        env_prefix="VENUE_",
    )
    url: VenueUrl
    token: SecretStr
```

- Construct each independently deployed configuration once at its boundary; reuse that immutable fact in dependent constructions.
- Type every non-secret field as a semantic scalar or value object.
- Use `SecretStr` for credentials and reveal it only while constructing the concrete client that consumes it.
- Put source names in settings aliases or `env_prefix`.
- Validate every default and make its omission meaning explicit.
- Inject the constructed config or the capability constructed from it; never re-read the environment.

## Do Not

- call `os.environ` outside `BaseSettings`
- use a settings dictionary, global singleton, or module-level primitive
- type a secret as `str`
- log, serialize, derive, or return a revealed secret
- mix deployment input with mutable runtime state

## Prove

In an isolated process environment, construct every required variable, omit each required variable once, and provide one malformed value per field. Assert defaults, source precedence, environment names, and masked `repr`. Search program source for `get_secret_value()` and require every use to be at concrete capability construction at the boundary, never in a domain derivation or a program-owned startup procedure.
