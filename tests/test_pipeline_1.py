## GraphK - Framework for Graph programming.
## Tests for Pipeline elements - Gate, Node, BranchNode
##
# Copyright (c) 2025, Dr. Fernando Koch
#    http://github.com/kochf1/graphk
#

import os
import json
from typing import Iterator, Any
from owlmind.graphk import Node, Gate, BranchNode

class ExperimentNode(Node):
    def ping(self) -> bool: return True
    def info(self) -> dict: return {"type": "test"}
    def step(self) -> Iterator[Any]: yield "step-execution"

class ExperimentBranchNode(BranchNode):
    def ping(self) -> bool: return True
    def info(self) -> dict: return {"type": "test-branch"}
    def step(self) -> Iterator[Any]: yield "branch-execution"


# Dummy gate for testing
mock_gate = Gate(checkers=lambda x: True)

# ============================================================
#  TESTS / EXPERIMENTS
# ============================================================

if __name__ == "__main__":

    print(f"\n🚀 STARTED: [{os.path.basename(__file__)}].")

    ####
    ## Experiment 1 — Test Gates
    ####
    print("\nExperiment 1: Test Gates")
    g = Gate(checkers=[lambda s: s.get("val") > 5], strategy=Gate.ALL_MATCH)
    assert g.assess({"val": 10}) is True
    assert g.assess({"val": 2}) is False
    print("✅ Gate Assessment Logic Checked")

    ####
    ## Experiment 2 — Node Framework Tests
    ####
    print("\nExperiment 2: Node Framework Tests")

    # Test 2.1: Initialization via context Dict vs Kwargs
    # Verify that both sources merge correctly into public attributes
    node_init = ExperimentNode(context={"a": 1}, b=2)
    assert node_init.a == 1 and node_init.b == 2
    print("  2.1: context/Kwargs merging verified.")

    # Test 2.2: The Obfuscation Typo Fix
    # Verify self._obfuscate_ (with trailing underscore) works correctly
    node_obf = ExperimentNode(secret="shhh", public="hello")
    node_obf.obfuscate("secret")
    assert "secret" not in node_obf.context()
    assert "public" in node_obf.context()
    print("  2.2: Obfuscation (_) registry verified.")

    # Test 2.3: Conditional Parameter Mapping
    # Verify internal attributes are ONLY mapped if provided
    node_slim = ExperimentNode(user="minimalist")
    assert not hasattr(node_slim, '_condition_')
    assert not hasattr(node_slim, '_weight_')
    assert "user" in node_slim.context()
    print("  2.3: Conditional attribute mapping verified.")

    # Test 2.4: Protection against Overwrites
    # Verify that leading underscore protects framework logic from context() export
    # even if a user tries to inject a similarly named variable.
    node_prot = ExperimentNode(_test_internal_="hidden", normal="visible")
    assert "_test_internal_" not in node_prot.context()
    assert "normal" in node_prot.context()
    print("  2.4: Leading underscore context filter verified.")

    # Test 2.5: String Representation (__repr__)
    # Verify __repr__ returns the context string
    node_repr = ExperimentNode(role="agent")
    expected_repr = str(node_repr.context())
    assert repr(node_repr) == expected_repr
    print("  2.5: Node representation (repr) verified.")
    print("✅ Node Framework Tests")



    ####
    ## Experiment 3 — BranchNode Logic & Strategy
    ####
    print("\nExperiment 3: BranchNode Logic & Strategy")

    # Setup Checkers & Gates
    is_active = lambda s: s.get("status") == "active"
    gate_active = Gate(is_active)

    # 3.1: Selection Strategy (FIRST vs BEST)
    # FIX: Pass status="active" to the nodes so their internal Gate assessment passes
    n_low  = ExperimentNode(condition=gate_active, weight=10, name="low_node", status="active")
    n_high = ExperimentNode(condition=gate_active, weight=100, name="high_node", status="active")

    branch_first = ExperimentBranchNode(nodes=[n_low, n_high], strategy=BranchNode.SELECT_FIRST)
    branch_best  = ExperimentBranchNode(nodes=[n_low, n_high], strategy=BranchNode.SELECT_BEST)

    res_first = branch_first.select()
    res_best = branch_best.select()

    assert res_first is not None, "Branch FIRST returned None"
    assert res_first.name == "low_node"

    assert res_best is not None, "Branch BEST returned None"
    assert res_best.name == "high_node"
    print("  3.1: Selection strategies (FIRST vs BEST) verified.")

    # 3.2: Hierarchical Gating & Weights
    # n1: Fails (Gate False)
    # n2: Fails (Priority Low)
    # n3: Passes (No Gate) -> Weight 10
    # n4: Passes (Status Active) -> Weight 5
    n1 = ExperimentNode(condition=Gate(lambda s: False), weight=200, name="blocked")
    n2 = ExperimentNode(condition=Gate(lambda s: s.get("priority") == "high"), weight=50, name="priority_path", priority="low")
    n3 = ExperimentNode(weight=10, name="default_path") 
    n4 = ExperimentNode(condition=gate_active, weight=5, name="active_path", status="active")

    branch_complex = ExperimentBranchNode(
        nodes=[n1, n2, n3, n4], 
        strategy=BranchNode.SELECT_BEST
    )

    selected = branch_complex.select()
    assert selected.name == "default_path"
    print("  3.2: Hierarchical gating and multi-node filtering verified.")

    # 3.3: Strategy - SELECT_RANDOM
    n_a = ExperimentNode(name="A")
    n_b = ExperimentNode(name="B")
    branch_rand = ExperimentBranchNode(nodes=[n_a, n_b], strategy=BranchNode.SELECT_RANDOM)

    results = {branch_rand.select().name for _ in range(20)}
    assert "A" in results and "B" in results
    print("  3.4: SELECT_RANDOM distribution verified.")

    print("✅ BranchNode Framework Tests")
      

    print(f"\n🎉 SUCCESS!! [{os.path.basename(__file__)}] completed.")



