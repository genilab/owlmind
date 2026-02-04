##
## OwlMind Framework - experimentation environment for Generative Intelligence Systems.
## Basic tests for Ollama
##
# Copyright (c) 2025, Dr. Fernando Koch
#    https://github.com/genilab/owlmind
#

# pip install -e .
# python3 tests/test_models_1.py

# pip install -e .
# python3 tests/test_models_1.py

import os
import json
import logging
from dotenv import load_dotenv
from owlmind.models import Ollama

# ============================================================
#  TESTS / EXPERIMENTS
# ============================================================

if __name__ == "__main__":

    print(f"\n🚀 STARTED: [{os.path.basename(__file__)}].")

    # Load variables from .env into os.environ
    load_dotenv()

    # Retrieve with fallbacks
    ENV_SERVER = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ENV_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
    Ollama.DEFAULT_LOG_LEVEL = logging.DEBUG

    ####
    ## Experiment 1 — Env Injection & Sparse Config
    ####
    print("\nExperiment 1: Env Injection & Sparse Config Visualization")

    model = Ollama(url=ENV_SERVER, model=ENV_MODEL, temperature=0.5)

    info = model.info()
    context = info["context"]

    # Verify None-filtering
    assert "url" in context
    assert "temperature" in context
    assert "seed" not in context

    # Framework internals must not leak
    assert "_client_" not in context
    assert "_models_cache_" not in context

    print(f"Server detected: {model.url}")
    print(json.dumps(info, indent=2))
    print("✅ CHECKED")

    ####
    ## Experiment 2 — Model Listing & Connectivity
    ####
    print("\nExperiment 2: Model Listing & Connectivity")

    info = model.info()
    print(f"Status: {info['status']}")

    assert hasattr(model, "_models_cache_")

    if info["status"] == "online":
        assert isinstance(info["models"], list)
        if len(info["models"]) == 0:
            print("⚠️ ALERT: Connection successful but list is empty. Check OLLAMA_HOST.")
        else:
            print(f"✅ Found {len(info['models'])} models.")

    print("✅ CHECKED")

    ####
    ## Experiment 3 — Hello World Request (payload)
    ####
    print("\nExperiment 3: Hello World Request")

    model.payload = "Say 'Hello OwlMind!'"

    if model.ping():
        print(f"Sending request to {model.model}...")

        for chunk in model.step():
            print(f"Yield: {chunk}")

        # Payload should now contain the response
        assert model.payload is not None
        assert "Hello" in model.payload

        # Payload must be visible in context
        ctx = model.context()
        assert "payload" in ctx

        print(f"Final Payload: {model.payload}")
    else:
        print("⚠️ Skipping request: Server offline.")

    print("✅ CHECKED")

    ####
    ## Experiment 4 — Creative Variation (High Temp)
    ####
    print("\nExperiment 4: Creative Variation (High Temp)")

    model = Ollama(
        url=ENV_SERVER,
        model=ENV_MODEL,
        temperature=1.5,
        log_level=Ollama.LOG_DEBUG
    )

    model.payload = "Write a one-sentence surrealist poem."
    for _ in model.step():
        pass

    context = model.info()["context"]

    assert context["temperature"] == 1.5
    assert "payload" in context

    print(f"Captured Payload: {model.payload}")
    print("✅ CHECKED")

    ####
    ## Experiment 5 — Precise Variation (Low Temp + Seed)
    ####
    print("\nExperiment 5: Precise Variation (Low Temp + Seed)")

    model = Ollama(
        url=ENV_SERVER,
        model=ENV_MODEL,
        temperature=0.0,
        seed=42,
        log_level=Ollama.LOG_DEBUG
    )

    model.payload = "What is the square root of 144?"

    for chunk in model.step():
        print(f"Yield: {chunk}")

    ctx = model.context()
    assert ctx["seed"] == 42
    assert "payload" in ctx

    print("✅ CHECKED")

    ####
    ## Experiment 6 — Long Context Configuration
    ####
    print("\nExperiment 6: Long Context Configuration")

    model = Ollama(
        url=ENV_SERVER,
        model=ENV_MODEL,
        num_ctx=8192,
        repeat_penalty=1.2
    )

    model.payload = "Explain the difference between a Class and an Instance in Python."
    for _ in model.step():
        pass

    assert model.num_ctx == 8192
    print(f"Context verified: {model.num_ctx} tokens.")
    print("✅ CHECKED")

    ####
    ## Experiment 7 — System Prompt Override
    ####
    print("\nExperiment 7: System Prompt Override")

    model = Ollama(
        url=ENV_SERVER,
        model=ENV_MODEL,
        system="Talk like a pirate"
    )

    model.payload = "Where is the treasure?"

    for chunk in model.step():
        print(f"Yield: {chunk}")

    assert "payload" in model.context()
    print("✅ CHECKED")

    ####
    ## Experiment 8 — Full Parameter Blast (Stress Test)
    ####
    print("\nExperiment 8: Full Parameter Blast")

    params = {
        "temperature": 0.9,
        "top_p": 0.8,
        "top_k": 20,
        "num_predict": 50,
        "repeat_penalty": 1.1,
        "seed": 99
    }

    model = Ollama(url=ENV_SERVER, model=ENV_MODEL, **params)
    model.payload = "Give me a 5-word sci-fi writing prompt."

    for _ in model.step():
        pass

    ctx = model.context()
    expected_params = {
        "temperature", "top_p", "top_k",
        "num_predict", "repeat_penalty", "seed"
    }

    actual_params = {
        k for k in ctx
        if k in model.OLLAMA_PARAMS and ctx[k] is not None
    }

    assert actual_params == expected_params
    assert "payload" in ctx

    print("Full context export:")
    print(json.dumps(ctx, indent=2))
    print("✅ CHECKED")

    print(f"\n🎉 SUCCESS!! [{os.path.basename(__file__)}] completed.")
