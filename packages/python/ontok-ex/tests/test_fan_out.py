from pytest import fail

from ontok.ex import BeginningCompletion, BranchesActivated
from ontok.ex.execution import BeginningCompletedExecution


def test_one_completion_activates_both_independent_branches(
    beginning_completion: BeginningCompletion,
    branches: BeginningCompletedExecution,
) -> None:
    emission: BranchesActivated = branches.emission

    if emission.left.prerequisite is not beginning_completion:
        fail("LeftWork was not activated by BeginningCompletion.")
    if emission.right.prerequisite is not beginning_completion:
        fail("RightWork was not activated by BeginningCompletion.")
