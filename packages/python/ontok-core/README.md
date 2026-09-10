# ontok-core

The type-native Python reference package for `spec/ontok-core.xml`.

## Namespace

`ontok.core`

## Responsibility

Core realizes ONTOK's universal organizational type system and depends on no other ONTOK package. Extension packages may depend on Core; Core never depends on an extension.

## Realization

`NodeId`, `Node`, and `Connection` realize the structural foundation. `Entity`, `Relation`, `State`, and `Event`, together with their temporal, memorialization, and causation structures, realize those portions of organizational reality. `Role` realizes the office through which an Entity acts. `Goal` realizes an intended end that goes on an Entity. `Action` realizes declared work through a Role toward a Goal. `Work` realizes a persistent undertaking of an Action. `Concept` realizes what a declaration means. `Context` realizes the States that constitute a situation. `Rule` realizes a constraint on declared work within a Context.
