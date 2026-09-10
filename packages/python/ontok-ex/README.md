# ontok-ex

The type-native Python reference package for `spec/ontok-ex.xml`.

## Namespace

`ontok.ex`

## Construction graph

`ontok-ex` is an event-driven execution algebra built directly from ONTOK. A Program declares
exact Work. An ExecutionRequest is the trigger. Activation is enabled Work. Completion is
performed Work. Each arrival constructs the next immutable execution fact and its emission.

```text
ExecutionRequest
└── Execution
    └── BeginningActivation
        └── BeginningCompletion
            ├── LeftActivation
            │   └── LeftCompletion
            └── RightActivation
                └── RightCompletion
                    └── BranchesCompleted
                        └── JoinedActivation
                            └── JoinedCompletion
                                └── TerminalExecution
```

`Program` is declaration only. Runtime identity and time arrive on `ExecutionRequest` and
Completion facts; the package generates neither. Exact Activation refinements own exact Work
and prerequisite fields. Every Activation derives and serializes direct execution correlation
from its originating request. `BranchesCompleted` is the required heterogeneous product for the
join, so JoinedActivation cannot exist without both exact branch Completions.

## Transport binding

A bus binding connects two typed constructions:

- `ExecutionRequest` constructs `Execution`, whose emission carries BeginningActivation.
- An exact Completion and exact current state construct an arrival, whose facts are the successor
  execution state and emission.

The package has no bus protocol, callback, service, registry, readiness classifier, or runner
loop. A terminal Completion recursively contains the complete proof that the Program ran.
