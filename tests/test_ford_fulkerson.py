"""
Tests unitaires — Ford-Fulkerson (Edmonds-Karp) et coupe minimale.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.residual_graph import ResidualGraph
from algorithms.ford_fulkerson import ford_fulkerson, find_min_cut
from algorithms.negative_cycle import assert_no_negative_cycle


def build_simple_graph():
    """0→1→3 et 0→2→3, capacités 1. Max flow = 2."""
    g = ResidualGraph(4)
    g.add_arc(0, 1, 1)
    g.add_arc(0, 2, 1)
    g.add_arc(1, 3, 1)
    g.add_arc(2, 3, 1)
    return g


def build_pathological_graph():
    """
    Graphe pathologique pour DFS (deux chemins parallèles de cap 100, arc croisé cap 1).
    Avec BFS (Edmonds-Karp), résolu efficacement. Max flow = 200.
    """
    g = ResidualGraph(4)
    g.add_arc(0, 1, 100)
    g.add_arc(0, 2, 100)
    g.add_arc(1, 3, 100)
    g.add_arc(2, 3, 100)
    g.add_arc(1, 2, 1)
    return g


def build_bipartite_graph():
    """
    Couplage biparti : 4 nœuds gauche, 4 nœuds droite.
    Couplage parfait possible → max flow = 4.
    """
    g = ResidualGraph(10)
    source, sink = 0, 9
    for left in range(1, 5):
        g.add_arc(source, left, 1)
    for right in range(5, 9):
        g.add_arc(right, sink, 1)
    g.add_arc(1, 5, 1)
    g.add_arc(2, 6, 1)
    g.add_arc(3, 7, 1)
    g.add_arc(4, 8, 1)
    g.add_arc(1, 6, 1)
    g.add_arc(3, 6, 1)
    return g, source, sink


def test_simple_graph():
    g = build_simple_graph()
    assert_no_negative_cycle(g)
    mf = ford_fulkerson(g, 0, 3)
    assert mf == 2, f"Attendu 2, obtenu {mf}"
    print(f"  ✓ test_simple_graph : max flow = {mf}")


def test_max_flow_equals_min_cut_simple():
    g = build_simple_graph()
    mf = ford_fulkerson(g, 0, 3)
    S, cut_arcs = find_min_cut(g, 0)
    cut_cap = sum(cap for _, _, cap in cut_arcs)
    assert mf == cut_cap, f"Max-Flow ({mf}) ≠ Min-Cut ({cut_cap})"
    print(f"  ✓ test_max_flow_equals_min_cut_simple : {mf} = {cut_cap}")


def test_pathological_graph():
    g = build_pathological_graph()
    assert_no_negative_cycle(g)
    mf = ford_fulkerson(g, 0, 3)
    assert mf == 200, f"Attendu 200, obtenu {mf}"
    print(f"  ✓ test_pathological_graph : max flow = {mf}")


def test_max_flow_equals_min_cut_pathological():
    g = build_pathological_graph()
    mf = ford_fulkerson(g, 0, 3)
    S, cut_arcs = find_min_cut(g, 0)
    cut_cap = sum(cap for _, _, cap in cut_arcs)
    assert mf == cut_cap, f"Max-Flow ({mf}) ≠ Min-Cut ({cut_cap})"
    print(f"  ✓ test_max_flow_equals_min_cut_pathological : {mf} = {cut_cap}")


def test_bipartite_max_matching():
    g, source, sink = build_bipartite_graph()
    mf = ford_fulkerson(g, source, sink)
    assert mf == 4, f"Attendu 4, obtenu {mf}"
    S, cut_arcs = find_min_cut(g, source)
    cut_cap = sum(cap for _, _, cap in cut_arcs)
    assert mf == cut_cap
    print(f"  ✓ test_bipartite_max_matching : max flow = {mf}")


def test_no_path():
    """Graphe déconnecté : sink inatteignable → max flow = 0."""
    g = ResidualGraph(3)
    g.add_arc(0, 1, 5)
    mf = ford_fulkerson(g, 0, 2)
    assert mf == 0, f"Attendu 0, obtenu {mf}"
    print(f"  ✓ test_no_path : max flow = {mf}")


def test_single_arc():
    g = ResidualGraph(2)
    g.add_arc(0, 1, 7)
    mf = ford_fulkerson(g, 0, 1)
    assert mf == 7, f"Attendu 7, obtenu {mf}"
    print(f"  ✓ test_single_arc : max flow = {mf}")


if __name__ == "__main__":
    print("=== Tests Ford-Fulkerson ===")
    test_simple_graph()
    test_max_flow_equals_min_cut_simple()
    test_pathological_graph()
    test_max_flow_equals_min_cut_pathological()
    test_bipartite_max_matching()
    test_no_path()
    test_single_arc()
    print("✓ Tous les tests Ford-Fulkerson passent.")
