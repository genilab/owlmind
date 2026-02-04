
##
## OwlMind Framework - experimentation environment for Generative Intelligence Systems.
## core/ollama.py — Ollama-backed implementation of the Component interface.
##
# Copyright (c) 2025, The Generative Intelligence Lab
#    https://github.com/genilab/owlmind
#
# Disclosure:
# This framework was developed using a 'vibe coding' . AI-synthesized logic was 
# subjected to human review and manual refinement to guarantee functional 
# integrity and structural clarity.
#

import logging
import ollama
from typing import Optional, Mapping, Any, Iterator
from owlmind.core import Component


class Ollama(Component):
    """
    Implementation of Ollama model access component.
    Configuration and parameters are strictly managed via attributes.
    """

    DEFAULT_SERVER = "http://localhost:11434"
    DEFAULT_MODEL = "llama3"
    DEFAULT_LOG_LEVEL = logging.INFO

    OLLAMA_PARAMS = {
        "temperature": None, "top_p": None, "seed": None,
        "num_ctx": None, "num_predict": None, "repeat_penalty": None,
        "top_k": None, "stop": None, "system": None
    }

    def __init__(
        self,
        context: Optional[Mapping[str, Any]] = None,
        *,
        log_level: int = DEFAULT_LOG_LEVEL,
        **kwargs: Any,
    ):
        # Internal framework storage
        self._models_cache_ = None
        self._client_ = None

        # Initialize Component (logging, context, payload, etc.)
        super().__init__(context=context, log_level=log_level, **kwargs)

        # Ensure public config attributes exist
        if not hasattr(self, "url"):
            self.url = self.DEFAULT_SERVER
        if not hasattr(self, "model"):
            self.model = self.DEFAULT_MODEL

        # Map optional Ollama parameters into context
        for param, default_value in self.OLLAMA_PARAMS.items():
            if not hasattr(self, param):
                setattr(self, param, default_value)

        # Initialize Ollama client
        self._client_ = ollama.Client(host=self.url)

        return

    def ping(self) -> bool:
        """Health check for Ollama server."""
        try:
            self._client_.list()
            return True
        except Exception as e:
            self.log(f"Ping failed at {self.url}: {e}", level=self.LOG_WARNING)
            return False

    def info(self) -> dict:
        """Capability reporting including available models and parameters."""
        if self._models_cache_ is None:
            try:
                response = self._client_.list()
                models_list = getattr(response, "models", response.get("models", []))
                self._models_cache_ = [
                    getattr(m, "model", getattr(m, "name", m.get("model", m.get("name"))))
                    for m in models_list if m
                ]
            except Exception:
                self._models_cache_ = []

        clean_context = {
            k: v for k, v in self.context().items() if v is not None
        }

        return {
            "status": "online" if self.ping() else "offline",
            "context": clean_context,
            "models": self._models_cache_,
            "parameters": list(self.OLLAMA_PARAMS.keys()),
        }


    def step(self) -> Iterator[str]:
        """
        Execution: Performs LLM inference.
        Expects `payload` to contain the prompt.
        """
        # Fail fast: no payload
        if self.payload is None:
            self.log("Step skipped: No payload provided.", level=self.LOG_WARNING)
            yield "No payload found."
            return

        # Prepare Ollama options
        options = {
            p: getattr(self, p)
            for p in self.OLLAMA_PARAMS
            if getattr(self, p) is not None
        }

        self.log(f"Inference: {self.model} @ {self.url}", level=self.LOG_DEBUG)
        self.log(f"Parameters: {options}", level=self.LOG_DEBUG)

        try:
            response = self._client_.generate(
                model=self.model,
                prompt=self.payload,
                options=options,
            )
            result = response.get("response", "")
            self.payload = result  # 🔁 propagate via context
        except Exception as e:
            self.log(f"Ollama Error: {e}", level=self.LOG_ERROR)
            result = f"Error: {str(e)}"
            self.payload = result

        yield self.payload
        return