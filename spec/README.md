# ONTOK Specification

This directory contains ONTOK's implementation-independent semantic specifications.

## `ontok-*.xml`

Every `ontok-*.xml` file defines one semantic module:

- `ontok-core.xml` defines the universal organizational type system.
- `ontok-vsm.xml` defines value streams as compositions of organizational action.
- `ontok-scim.xml` aligns SCIM identity resources with ONTOK.
- `ontok-st.xml` defines Semantic Topology as the structure of meaning among Concepts.
- `ontok-ex.xml` defines transport-independent event-driven execution of Work.
- Future `ontok-<module>.xml` files may define additional standard capabilities.

There may be any number of modules. This allows ONTOK to acquire major organizational capabilities without enlarging Core or forcing every organization to adopt every capability.

## Module discipline

Every module declares its imports explicitly. Dependencies are one-way: Core imports nothing, a module may import Core or earlier modules, and an imported module never acquires knowledge of an importing module.

A module contains only the meanings it introduces:

- names and descriptions define semantic intent;
- `refines` expresses only a true semantic *is-a* relationship;
- fields express mandatory dependencies on other constructs;
- supporting scalars, values, unions, and relations make primitive construction complete;
- derivations state facts implied by constructed fields;
- laws define consequences that cannot be expressed by structure alone;
- alignments connect external standards without reproducing them.

The specification files are not serialized organizational graphs and are not substitutes for external standards. They define the language in which organizational programs are declared.

## Executable specification

Each XML module and its corresponding type-native reference package form one executable specification. The XML defines meaning independently of any host language; the package realizes that meaning through types whose successful construction makes invalid declarations unrepresentable.

Each language realization belongs under `packages/<language>/` and uses that language's native workspace and packaging tools. The Python packages live under `packages/python/` as independently publishable members of one uv workspace sharing the `ontok` namespace.

Package dependencies mirror XML imports exactly in every language: Core depends on no ONTOK package, while VSM, SCIM, ST, and EX depend one-way on Core.

Only `README.md` and `ontok-*.xml` source files belong in this directory. Implementations, tests, generated files, and build artifacts belong elsewhere.
