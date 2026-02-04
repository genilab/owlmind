##
## OwlMind Framework - experimentation environment for Generative Intelligence Systems.
## core/component.py — Abstract base definition for generative workflow components.
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
from typing import Any, Optional, Mapping, Union
from abc import ABC
from owlmind.graphk import Node


##
## COMPONENT
##

class Component(Node, ABC):
    """
    Base class for framework components with managed I/O and logging.
    """
    
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    # Log Levels as Constants
    LOG_DEBUG = logging.DEBUG
    LOG_INFO = logging.INFO
    LOG_WARNING = logging.WARNING
    LOG_ERROR = logging.ERROR
    LOG_CRITICAL = logging.CRITICAL

    def __init__(
        self,
        context: Optional[Mapping[str, Any]] = None,
        *,
        log_level: int = LOG_CRITICAL,
        **kwargs: Any,
    ):
        # 1. Setup logging infrastructure
        if not logging.getLogger().hasHandlers(): 
            logging.basicConfig(level=logging.WARNING, format=self.LOG_FORMAT)
        
        # Internal framework storage using _name_ convention
        self._logger_ = logging.getLogger(self.__class__.__name__)
  
        # Initialize Node (this handles _condition_, _weight_, etc.)
        super().__init__(context=context, **kwargs)

        # 2. Set the log level using the property setter
        self.log_level = log_level

        # 3. Obfuscate framework attributes to keep session() clean
        self.obfuscate(['log_level'])

        return

    @property
    def payload(self) -> Any:
        return self.__dict__.get('payload', None)

    @payload.setter
    def payload(self, payload: Any) -> None:
        self.__dict__['payload'] = payload

    @property
    def log_level(self) -> int: 
        return self._logger_.level

    @log_level.setter
    def log_level(self, level: Union[int, str]) -> None:
        val = getattr(logging, level.upper(), None) if isinstance(level, str) else level
        if isinstance(val, int): 
            self._logger_.setLevel(val)
        return

    def log(self, message: str, level: int = LOG_INFO) -> None:
        self._logger_.log(level, message)

  