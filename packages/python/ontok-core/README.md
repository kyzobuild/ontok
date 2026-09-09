# ontok-core

The type-native Python reference package for `spec/ontok-core.xml`.

## Namespace

`ontok.core`

## Responsibility

Core realizes ONTOK's universal organizational type system and depends on no other ONTOK package. Extension packages may depend on Core; Core never depends on an extension.

## Status

`NodeId`, `Node`, and `Connection` realize the structural foundation. `Entity`, `Relation`, and `Event`, together with their temporal, memorialization, and causation structures, realize those portions of organizational reality. `State` is an empty sortal. `Role` realizes the office through which an Entity acts. Goal, Action, and later Core layers remain unimplemented until their semantic definitions and dependencies are complete.
