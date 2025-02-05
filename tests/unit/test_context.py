from owlmind.context import Context
import pytest

pytestmark = pytest.mark.unit


def test__addition_overload():
    ctx = Context({"key": "value"})
    ctx += {"new_key": "new_value"}

    assert ctx["key"] == "value"
    assert ctx["new_key"] == "new_value"


def test_contains_overload_returns_false_on_non_context_type():
    ctx = Context({"key": "value"})
    test = {"key": "value"}

    assert test not in ctx


def test_contains_overload_returns_true_on_exact_match():
    ctx = Context({"key": "value"})
    ctx_two = Context({"key": "value"})

    assert ctx_two in ctx


@pytest.mark.parametrize("wildcard", ["*", "_"])
def test_contains_overload_returns_true_on_wildcard_match(wildcard: str):
    ctx = Context({"key": "value"})
    ctx_two = Context({"key": wildcard})

    assert ctx_two in ctx


@pytest.mark.parametrize(
    "pattern, target, expected",
    [
        ("r/value", "value", True),
        ("r/value/", "value", True),
        ("r/value", "owlmind", False),
    ],
)
def test_contains_overload_returns_correct_value_on_regex(pattern, target, expected):
    ctx = Context({"key": target})
    ctx_two = Context({"key": pattern})

    assert (ctx_two in ctx) == expected
