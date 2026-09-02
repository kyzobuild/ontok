from importlinter.cli import lint_imports
from pytest import fail


def test_modules_follow_workspace_dependency_graph() -> None:
    if lint_imports(no_cache=True, no_logo=True) != 0:
        fail("ONTOK package imports violate the workspace dependency graph.")
