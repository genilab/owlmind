##
## GraphK - Framework for Graph programming.
## node.py — data structures for Nodes in Processing Lines
#            Include: Gate, Node, BrachNode.
##
# Copyright (c) 2025, Dr. Fernando Koch
#    http://github.com/kochf1/graphk
#
# Disclosure:
# This code was developed through 'vibe coding'. Certain components
# required manual implementation, and human-in-the-loop review and refinement
# were applied throughout the project.
#

import random
from abc import ABC, abstractmethod
from typing import Union, Callable, List, Any, Iterator, Iterable, Optional, Mapping, Sequence

Checker = Callable[[Any], bool]

##
## GATE
##

class Gate:
    """
    Validation Structurs.
    """
    # Strategy Constants
    ALL_MATCH = 1      # Logical AND
    ANY_MATCH = 2      # Logical OR
    ONE_ONE_MATCH = 3  # Exclusive OR / Single match

    def __init__(
        self,
        checkers: Union[Checker, Iterable[Checker]],
        strategy: int = ALL_MATCH,
    ):
        self.checkers: List[Checker] = (
            list(checkers) if isinstance(checkers, (list, tuple)) else [checkers]
        )
        self.strategy: int = strategy

    def assess(self, context: Any) -> bool:
        """
        Executes the assessment logic against the provided context (dict)
        """
        # Convert checkers into a generator of booleans
        results = (func(context) for func in self.checkers)

        if self.strategy == self.ALL_MATCH:
            return all(results)
        
        if self.strategy == self.ANY_MATCH:
            return any(results)
        
        if self.strategy == self.ONE_ONE_MATCH:
            # Returns True if exactly one checker returns True
            return list(results).count(True) == 1

        return False
    
##
## NODE
##

class Node(ABC):
    """
    Base Node.
    """

    def __init__(
        self,
        context: Optional[Mapping[str, Any]] = None,
        *,
        condition: Optional[Gate] = None,
        validation: Optional[Gate] = None,
        weight: Optional[int] = None,
        next: Optional[Any] = None,
        **kwargs: Any,
    ):
        
        # Initialize the obfuscation set
        self._obfuscate_ = set()

        # Map internal attributes only if they are provided
        if condition is not None: self._condition_ = condition
        if validation is not None: self._validation_ = validation
        if weight is not None: self._weight_ = weight
        if next is not None: self._next_ = next
        
        # Process session and dynamic kwargs in one pass
        for key, value in ((context or {}) | kwargs).items(): 
            setattr(self, key, value)
        return

    def __repr__(self):
        return str(self.context())

    def obfuscate(self, keys: Union[str, Iterable[str]]) -> None:
        """Adds keys to the obfuscation list to hide it from context exports."""
        self._obfuscate_.update([keys] if isinstance(keys, str) else keys)
        return

    def context(self) -> dict:
        """Returns public state; filters internal and obfuscated keys."""
        return {
            k: v for k, v in self.__dict__.items()
            if not k.startswith('_') and k not in self._obfuscate_
        }

    @abstractmethod
    def ping(self) -> bool:
        """Health check / Connectivity test."""
        pass

    @abstractmethod
    def info(self) -> dict:
        """Metadata and capability reporting."""
        pass

    @abstractmethod
    def step(self) -> Iterator[Any]:
        """Execution logic; must return iterator."""
        pass


##
## BRANCH NODE
##

class BranchNode(Node, ABC):
    """
    Branched nodes.
    """

    # Selection strategies
    SELECT_FIRST = 0
    SELECT_RANDOM = 1
    SELECT_BEST = 2

    def __init__(
        self,
        nodes: Sequence[Node],
        strategy: int = SELECT_FIRST,
        context: Optional[Mapping[str, Any]] = None,
        **kwargs: Any,
    ):
        super().__init__(session=context, **kwargs)
        self._nodes_ = nodes
        self._strategy_ = strategy
        return 

    def select(self) -> Optional[Node]:
        """
        Filters nodes based on their _condition_ Gate and applies the selection strategy.
        """
        selected_node = None

        # 1. Filter valid nodes using the _condition_ gate
        valid_nodes = []
        for node in self._nodes_:
            # If a gate exists, we assess it; otherwise, the path is open (default True)
            is_valid = True
            condition: Optional[Gate] = getattr(node, '_condition_', None)
            if condition is not None:
                is_valid = condition.assess(node.context())
            
            if is_valid:
                valid_nodes.append(node)

        # Fail fast: No valid paths available
        if not valid_nodes:
            return None

        # 2. Apply Selection Strategy
        if self._strategy_ == self.SELECT_FIRST:
            selected_node = valid_nodes[0]

        elif self._strategy_ == self.SELECT_RANDOM:
            selected_node = random.choice(valid_nodes)

        elif self._strategy_ == self.SELECT_BEST:
            # Selection based on the _weight_ attribute
            selected_node = max(valid_nodes, key=lambda n: getattr(n, '_weight_', 0))

        return selected_node