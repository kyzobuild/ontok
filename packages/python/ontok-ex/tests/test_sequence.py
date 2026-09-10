from pytest import fail

from ontok.ex import BeginningCompletion, BeginningCompletionArrival, Execution, ExecutionRequest


def test_request_then_completion_constructs_the_next_execution(
    execution_request: ExecutionRequest,
    beginning_completion: BeginningCompletion,
) -> None:
    execution = Execution(request=execution_request)
    progressed = BeginningCompletionArrival(completion=beginning_completion)

    if execution.emission.activation.prerequisite is not execution_request:
        fail("The request did not construct its exact beginning Activation.")
    if execution.emission.activation.execution is not execution_request.id:
        fail("The Activation lost direct execution correlation.")
    if progressed.state.completion is not beginning_completion:
        fail("The Completion did not construct the next execution.")
    if progressed.state.left.prerequisite is not beginning_completion:
        fail("The next Work does not depend on the exact prior Completion.")
