##
## OwlMind Framework - experimentation environment for Generative Intelligence Systems.
## component.py — XXX
##
#
# Copyright (c) 2025, The Generative Intelligence Lab
#
#    https://github.com/genilab/owlmind
#
# Disclosure:
# This code was developed through 'vibe coding'. Certain components
# required manual implementation, and human-in-the-loop review and refinement
# were applied throughout the project.
#

from abc import ABC, abstractmethod
from typing import Iterator, Any

class Component(ABC):
    """
    Base abstract class for all OwlMind building blocks.
    A component represents a single unit of logic in the 
    Generative Intelligence workflow.
    """

    def __init__(self, context:dict):
        # The context dictionary acts as the 'shared memory' 
        # for the component during execution.
        self.context = context
        return

    @abstractmethod
    def ping(self) -> bool:
        """ Check Connectivity """
        pass

    @abstractmethod
    def info(self) -> list:
        """Provide detailed environment or state information."""
        pass

    @abstractmethod
    def step(self) -> Iterator[Any]:
        """
        Execute one unit of work; Yields intermediate states.
        Reads from and modifies self.context to pass data to other components
        """
        pass

