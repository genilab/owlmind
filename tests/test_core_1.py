##
## OwlMind Framework - experimentation environment for Generative Intelligence Systems.
## Tests for core elements - Component
##
# Copyright (c) 2025, Dr. Fernando Koch
#    https://github.com/genilab/owlmind
#

# pip install -e .
# python3 tests/test_core_1.py

import os
import json
import logging
from typing import Iterator, Any
from owlmind.core import Component

# Concrete implementation for testing purposes
class MyComponent(Component):
    def ping(self) -> bool:
        return True

    def info(self) -> dict:
        return {"name": "TestComponent"}

    def step(self) -> Iterator[Any]:
        # simple passthrough / mutation example
        if self.payload is not None:
            self.payload = f"{self.payload}-processed"
        yield self.payload
        return


# ============================================================
#  TESTS / EXPERIMENTS
# ============================================================

if __name__ == "__main__":

    print(f"\n🚀 STARTED: [{os.path.basename(__file__)}].")

    ####
    ## Experiment 1 — Initialization & Logger Sync
    ####
    print("\nExperiment 1: Initialization & Logger Sync")
    comp = MyComponent(log_level="DEBUG", user_id="FK-2026")

    assert comp.log_level == MyComponent.LOG_DEBUG
    assert comp._logger_.level == logging.DEBUG
    assert hasattr(comp, "_logger_")

    print(json.dumps(comp.context(), indent=2))
    print("✅ CHECKED")

    ####
    ## Experiment 2 — Dynamic Level Updates
    ####
    print("\nExperiment 2: Dynamic Level Updates")
    comp = MyComponent(log_level=MyComponent.LOG_INFO)

    assert comp._logger_.level == logging.INFO

    comp.log_level = "WARNING"
    assert comp._logger_.level == MyComponent.LOG_WARNING
    assert comp.log_level == logging.WARNING

    print(f"Updated Level (int): {comp.log_level}")
    print("✅ CHECKED")

    ####
    ## Experiment 3 — context Cleanliness
    ####
    print("\nExperiment 3: context Cleanliness")
    comp = MyComponent(
        log_level=MyComponent.LOG_DEBUG,
        api_key="sk-12345",
        project="OwlMind"
    )
    comp.obfuscate("api_key")

    context_data = comp.context()

    assert "_logger_" not in context_data
    assert "log_level" not in context_data
    assert "api_key" not in context_data
    assert "project" in context_data

    print(json.dumps(context_data, indent=2))
    print("✅ CHECKED")

    ####
    ## Experiment 4 — Functional Logging Output
    ####
    print("\nExperiment 4: Functional Logging Output")
    logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', force=True)

    comp = MyComponent(log_level="DEBUG")

    print("Should see a DEBUG log below:")
    comp.log("This is a test log message at DEBUG level.", level=MyComponent.LOG_DEBUG)

    comp.log_level = MyComponent.LOG_ERROR
    print(f"Level is now: {comp.log_level} (ERROR)")
    print("Should NOT see a DEBUG log below:")
    comp.log("This message should be suppressed.", level=MyComponent.LOG_DEBUG)

    print("✅ CHECKED")

    ####
    ## Experiment 5 — payload Presence & Default Behavior
    ####
    print("\nExperiment 5: payload Presence & Default Behavior")
    comp = MyComponent()

    assert comp.payload is None
    assert "payload" not in comp.context()

    comp.payload = 123
    assert comp.payload == 123
    assert comp.context()["payload"] == 123

    print(json.dumps(comp.context(), indent=2))
    print("✅ CHECKED")

    ####
    ## Experiment 6 — payload Mutation During step()
    ####
    print("\nExperiment 6: payload Mutation During step()")
    comp = MyComponent(context={"payload": "data"})

    results = list(comp.step())

    assert results == ["data-processed"]
    assert comp.payload == "data-processed"

    print(f"Final payload: {comp.payload}")
    print("✅ CHECKED")

    ####
    ## Experiment 7 — payload Transfer Between Components
    ####
    print("\nExperiment 7: payload Transfer Between Components")

    comp_a = MyComponent(context={"payload": "payload"})
    comp_b = MyComponent()

    # simulate pipeline transfer
    comp_b.payload = comp_a.payload

    assert comp_b.payload == "payload"
    assert comp_b.context()["payload"] == "payload"

    print("Component A context:")
    print(json.dumps(comp_a.context(), indent=2))

    print("Component B context:")
    print(json.dumps(comp_b.context(), indent=2))

    print("✅ CHECKED: payload transferred successfully")

    ####
    ## Experiment 8 — Obfuscation Does NOT Affect payload
    ####
    print("\nExperiment 8: Obfuscation Does NOT Affect payload")

    comp = MyComponent(context={"payload": 999, "secret": "hidden"})
    comp.obfuscate("secret")

    ctx = comp.context()

    assert "payload" in ctx
    assert ctx["payload"] == 999
    assert "secret" not in ctx

    print(json.dumps(ctx, indent=2))
    print("✅ CHECKED")

    print(f"\n🎉 SUCCESS!! [{os.path.basename(__file__)}] completed.")

