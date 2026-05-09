# Tests detection cycles negatifs

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.residual_graph import ResidualGraph
from algorithms.negative_cycle import detect_negative_cycle, assert_no_negative_cycle


def test_no_cycle_positive_costs():
    """Tous les coûts positifs → pas de cycle négatif possible."""
    g = ResidualGraph(4)
    g.add_arc(0, 1, 10, cost=2)
    g.add_arc(1, 2, 10, cost=3)
    g.add_arc(2, 0, 10, cost=4)
    g.add_arc(0, 3, 10, cost=1)
    has_cycle, cycle = detect_negative_cycle(g)
    assert not has_cycle, f"Cycle inattendu : {cycle}"
    print(f"  ✓ test_no_cycle_positive_costs")


def test_negative_cycle_simple():
    """Cycle de coût 1+1-5 = -3 < 0 : cycle négatif détecté."""
    g = ResidualGraph(3)
    g.add_arc(0, 1, 10, cost=1)
    g.add_arc(1, 2, 10, cost=1)
    g.add_arc(2, 0, 10, cost=-5)
    has_cycle, cycle = detect_negative_cycle(g)
    assert has_cycle, "Cycle négatif non détecté"
    print(f"  ✓ test_negative_cycle_simple : cycle = {cycle}")


def test_assert_raises():
    """assert_no_negative_cycle lève AssertionError si cycle négatif présent."""
    g = ResidualGraph(3)
    g.add_arc(0, 1, 10, cost=1)
    g.add_arc(1, 2, 10, cost=1)
    g.add_arc(2, 0, 10, cost=-5)
    raised = False
    try:
        assert_no_negative_cycle(g)
    except AssertionError:
        raised = True
    assert raised, "AssertionError aurait dû être levée"
    print(f"  ✓ test_assert_raises")


if __name__ == "__main__":
    print("=== Tests Détection de Cycles Négatifs ===")
    test_no_cycle_positive_costs()
    test_negative_cycle_simple()
    test_assert_raises()
    print("✓ Tous les tests cycles négatifs passent.")
