# Tests Min Cost Flow (BF + Dijkstra)

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.residual_graph import ResidualGraph
from algorithms.min_cost_flow_bf import min_cost_flow_bellman_ford
from algorithms.min_cost_flow_dijkstra import min_cost_flow_dijkstra
from algorithms.negative_cycle import assert_no_negative_cycle


def build_simple_cost_graph():
    """5 noeuds, max flow = 10, cout total = 30."""
    g = ResidualGraph(5)
    g.add_arc(0, 1, 10, cost=2)
    g.add_arc(0, 2, 10, cost=4)
    g.add_arc(1, 3, 10, cost=1)
    g.add_arc(2, 3, 10, cost=3)
    g.add_arc(3, 4, 10, cost=0)
    g.add_arc(1, 2, 5,  cost=1)
    return g


def build_single_path_graph():
    """Un seul chemin 0→1→2, cap=5, cost=3+2=5. Max flow=5, coût=25."""
    g = ResidualGraph(3)
    g.add_arc(0, 1, 5, cost=3)
    g.add_arc(1, 2, 5, cost=2)
    return g


def build_parallel_paths_graph():
    """Deux chemins parallels, pour 3 unites cout = 3."""
    g = ResidualGraph(3)
    g.add_arc(0, 1, 3, cost=1)
    g.add_arc(1, 2, 3, cost=0)
    g.add_arc(0, 2, 3, cost=3)
    return g


def build_diamond_graph():
    """Diamant. Max flow = 8, cout = 24."""
    g = ResidualGraph(4)
    g.add_arc(0, 1, 4, cost=1)
    g.add_arc(0, 2, 4, cost=2)
    g.add_arc(1, 3, 4, cost=2)
    g.add_arc(2, 3, 4, cost=1)
    return g


def test_simple_cost_graph_bf():
    g = build_simple_cost_graph()
    assert_no_negative_cycle(g)
    flow, cost = min_cost_flow_bellman_ford(g, 0, 4)
    assert flow == 10, f"Attendu flow=10, obtenu {flow}"
    assert cost == 30, f"Attendu cost=30, obtenu {cost}"
    print(f"  ✓ test_simple_cost_graph_bf : flow={flow}, cost={cost}")


def test_simple_cost_graph_dijkstra():
    g = build_simple_cost_graph()
    assert_no_negative_cycle(g)
    flow, cost = min_cost_flow_dijkstra(g, 0, 4)
    assert flow == 10, f"Attendu flow=10, obtenu {flow}"
    assert cost == 30, f"Attendu cost=30, obtenu {cost}"
    print(f"  ✓ test_simple_cost_graph_dijkstra : flow={flow}, cost={cost}")


def test_bf_equals_dijkstra_simple():
    g1 = build_simple_cost_graph()
    g2 = build_simple_cost_graph()
    flow_bf, cost_bf = min_cost_flow_bellman_ford(g1, 0, 4)
    flow_dj, cost_dj = min_cost_flow_dijkstra(g2, 0, 4)
    assert flow_bf == flow_dj, f"Flows différents : BF={flow_bf}, Dijkstra={flow_dj}"
    assert cost_bf == cost_dj, f"Coûts différents : BF={cost_bf}, Dijkstra={cost_dj}"
    print(f"  ✓ test_bf_equals_dijkstra_simple : flow={flow_bf}, cost={cost_bf}")


def test_single_path():
    g = build_single_path_graph()
    flow, cost = min_cost_flow_bellman_ford(g, 0, 2)
    assert flow == 5 and cost == 25
    g2 = build_single_path_graph()
    flow2, cost2 = min_cost_flow_dijkstra(g2, 0, 2)
    assert flow2 == 5 and cost2 == 25
    print(f"  ✓ test_single_path : flow={flow}, cost={cost}")


def test_required_flow():
    """Envoyer exactement required_flow=3 unités, pas plus."""
    g = build_parallel_paths_graph()
    flow, cost = min_cost_flow_bellman_ford(g, 0, 2, required_flow=3)
    assert flow == 3, f"Attendu 3, obtenu {flow}"
    assert cost == 3, f"Attendu cost=3, obtenu {cost}"
    g2 = build_parallel_paths_graph()
    flow2, cost2 = min_cost_flow_dijkstra(g2, 0, 2, required_flow=3)
    assert flow2 == 3 and cost2 == 3
    print(f"  ✓ test_required_flow : flow={flow}, cost={cost}")


def test_diamond_graph():
    g1 = build_diamond_graph()
    g2 = build_diamond_graph()
    flow_bf, cost_bf = min_cost_flow_bellman_ford(g1, 0, 3)
    flow_dj, cost_dj = min_cost_flow_dijkstra(g2, 0, 3)
    assert flow_bf == flow_dj == 8
    assert cost_bf == cost_dj == 24
    print(f"  ✓ test_diamond_graph : flow=8, cost=24")


def test_bf_equals_dijkstra_diamond():
    g1 = build_diamond_graph()
    g2 = build_diamond_graph()
    assert min_cost_flow_bellman_ford(g1, 0, 3) == min_cost_flow_dijkstra(g2, 0, 3)
    print(f"  ✓ test_bf_equals_dijkstra_diamond : identiques")


if __name__ == "__main__":
    print("=== Tests Min Cost Flow ===")
    test_simple_cost_graph_bf()
    test_simple_cost_graph_dijkstra()
    test_bf_equals_dijkstra_simple()
    test_single_path()
    test_required_flow()
    test_diamond_graph()
    test_bf_equals_dijkstra_diamond()
    print("✓ Tous les tests Min Cost Flow passent.")
