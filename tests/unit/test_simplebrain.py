from owlmind.simplebrain import SimpleBrain
from owlmind.context import Context
import pytest

pytestmark = pytest.mark.unit

FAKE_RULES_PATH = "./tests/unit/fixtures/fakerules.csv"


def test_load():
    # this tests makes sure the rules csv is loaded correctly and makes sure the loaded messages
    # are in the context repo that the simplebrain agent has as an internal property

    # TODO: This test is really whiteboxy and needs to know way to much
    # about the internals, just suffer with it until we can start refactoring
    simplebrain = SimpleBrain(id="test-bot")
    simplebrain.load(FAKE_RULES_PATH)

    ctx = Context({"message": "hello"})
    ctx2 = Context({"message": "good morning"})

    # this context is not in the fake rules
    ctx3 = Context({"message": "Where is the bathroom?"})

    # the contains method actually mutates the context object we're checking
    # if you're thinking to yourself, thats madness, you're correct it is
    ctx in simplebrain.plans
    ctx2 in simplebrain.plans
    ctx3 in simplebrain.plans

    # these results match the rules found in the fake rules fixture
    assert ctx.best_result == "Hi there! How can I assist you today?"
    assert ctx2.best_result == "Good morning! How can I make your day better?"

    # this is the generic wildcard match for when a message is received with no better match
    assert ctx3.best_result == "I have no idea how to respond!"
