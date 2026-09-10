# ontok-ex

The type-native Python reference package for `spec/ontok-ex.xml`.

## Namespace

`ontok.ex`

## Responsibility

EX is the transport-independent event-driven executor for ONTOK Work. Trigger and Completion Events construct an immutable execution history that activates dependent Work exactly once and declares the execution active, blocked, or finished. It depends one-way on `ontok-core` and remains independent of other extension packages.

## Realization

An `ExecutionPlan` declares Work and Dependencies. An `ExecutionOrigin` constructs from its triggering Event. Each Completion constructs an `ExecutionProgression`, whose recursive derivations expose newly enabled Activations and an active, blocked, or finished status.

Construction is execution. EX has no callback, runner loop, client protocol, bus, or API. A transport only has to deliver constructed Events and publish derived Activations; the application performing a specific Action constructs its Completion.
