"""
Démonstration des algorithmes de flot implémentés dans ce projet.

Démos disponibles :
  1. Ford-Fulkerson — Max Flow + Min Cut
  2. Graphe d'affectation (Peter/Paul/Mary)
  3. Min Cost Flow — Bellman-Ford
  4. Min Cost Flow — Dijkstra + renormalisation
  5. Comparaison Bellman-Ford vs Dijkstra
  6. Détection de cycles négatifs
"""

from graph.residual_graph import ResidualGraph
from algorithms.ford_fulkerson import ford_fulkerson, find_min_cut, print_flow_result
from algorithms.min_cost_flow_bf import min_cost_flow_bellman_ford
from algorithms.min_cost_flow_dijkstra import min_cost_flow_dijkstra
from algorithms.negative_cycle import detect_negative_cycle, assert_no_negative_cycle


def demo_ford_fulkerson():
    """
    Ford-Fulkerson sur un graphe à 5 nœuds.

    Graphe :
      S→A: 10   A→C: 10
      S→B: 10   B→C: 10
      A→B: 1    C→T: 10

    Max flow attendu = 10 (bottleneck sur C→T).
    """
    print("\n" + "=" * 60)
    print("DEMO 1 : Ford-Fulkerson — Max Flow + Min Cut")
    print("=" * 60)

    # 0=S, 1=A, 2=B, 3=C, 4=T
    g = ResidualGraph(5)
    source, sink = 0, 4
    node_names = {0: 'S', 1: 'A', 2: 'B', 3: 'C', 4: 'T'}

    g.add_arc(0, 1, 10)
    g.add_arc(0, 2, 10)
    g.add_arc(1, 3, 10)
    g.add_arc(2, 3, 10)
    g.add_arc(3, 4, 10)
    g.add_arc(1, 2, 1)

    assert_no_negative_cycle(g)

    max_flow = ford_fulkerson(g, source, sink)
    print_flow_result(g, max_flow, source, sink, node_names)


def demo_assignment_graph():
    """
    Graphe d'affectation : 3 personnes, 5 projets, 3 tâches.

    Personnes : Peter, Paul, Mary
    Projets   : M, D, N, B, O
    Tâches    : Bob, Mike, Julia

    Structure :
      Source → Personne : cap 3
      Personne → Projet : cap 1 (affectation)
      Projet  → Tâche  : cap selon le projet
      Tâche   → Sink   : cap selon la demande

    Max flow attendu = 7.
    """
    print("\n" + "=" * 60)
    print("DEMO 2 : Graphe d'affectation Peter/Paul/Mary")
    print("=" * 60)

    # 0=Source, 1=Peter, 2=Paul, 3=Mary,
    # 4=M, 5=D, 6=N, 7=B, 8=O,
    # 9=Bob, 10=Mike, 11=Julia, 12=Sink
    g = ResidualGraph(13)
    source, sink = 0, 12
    node_names = {
        0: 'Source', 1: 'Peter', 2: 'Paul', 3: 'Mary',
        4: 'M', 5: 'D', 6: 'N', 7: 'B', 8: 'O',
        9: 'Bob', 10: 'Mike', 11: 'Julia', 12: 'Sink'
    }

    g.add_arc(0, 1, 3)
    g.add_arc(0, 2, 3)
    g.add_arc(0, 3, 3)

    g.add_arc(1, 4, 1)   # Peter → M
    g.add_arc(1, 5, 1)   # Peter → D
    g.add_arc(1, 6, 1)   # Peter → N
    g.add_arc(2, 4, 1)   # Paul  → M
    g.add_arc(2, 7, 1)   # Paul  → B
    g.add_arc(2, 8, 1)   # Paul  → O
    g.add_arc(3, 5, 1)   # Mary  → D
    g.add_arc(3, 6, 1)   # Mary  → N
    g.add_arc(3, 8, 1)   # Mary  → O

    g.add_arc(4, 9,  2)  # M → Bob
    g.add_arc(5, 10, 2)  # D → Mike
    g.add_arc(6, 11, 1)  # N → Julia
    g.add_arc(7, 9,  2)  # B → Bob
    g.add_arc(8, 11, 2)  # O → Julia

    g.add_arc(9,  sink, 3)
    g.add_arc(10, sink, 2)
    g.add_arc(11, sink, 2)

    assert_no_negative_cycle(g)

    max_flow = ford_fulkerson(g, source, sink)
    print(f"\nMax flow (affectation) = {max_flow}  (attendu : 7)")

    S, cut_arcs = find_min_cut(g, source)
    cut_cap = sum(cap for _, _, cap in cut_arcs)
    print(f"Min Cut capacity = {cut_cap}  (doit = {max_flow})")
    assert cut_cap == max_flow
    print("✓ Max-Flow = Min-Cut vérifié")


def demo_min_cost_flow_bellman_ford():
    """
    Min Cost Flow avec Bellman-Ford.

    Graphe :
      0→1: cap=10, cost=2   1→3: cap=10, cost=1
      0→2: cap=10, cost=4   2→3: cap=10, cost=3
      1→2: cap=5,  cost=1   3→4: cap=10, cost=1

    Chemin le moins cher : 0→1→3→4, coût/unité = 4.
    Max flow = 10, coût total = 40.
    """
    print("\n" + "=" * 60)
    print("DEMO 3 : Min Cost Flow — Bellman-Ford")
    print("=" * 60)

    g = ResidualGraph(5)
    source, sink = 0, 4

    g.add_arc(0, 1, 10, cost=2)
    g.add_arc(0, 2, 10, cost=4)
    g.add_arc(1, 3, 10, cost=1)
    g.add_arc(2, 3, 10, cost=3)
    g.add_arc(3, 4, 10, cost=1)
    g.add_arc(1, 2, 5,  cost=1)

    assert_no_negative_cycle(g)

    flow, cost = min_cost_flow_bellman_ford(g, source, sink)
    print(f"Flot total : {flow}")
    print(f"Coût total : {cost}")


def demo_min_cost_flow_dijkstra():
    """
    Même graphe que Demo 3, résolu avec Dijkstra + potentiels de Johnson.
    Doit donner le même résultat que Bellman-Ford.
    """
    print("\n" + "=" * 60)
    print("DEMO 4 : Min Cost Flow — Dijkstra + Renormalisation")
    print("=" * 60)

    g = ResidualGraph(5)
    source, sink = 0, 4

    g.add_arc(0, 1, 10, cost=2)
    g.add_arc(0, 2, 10, cost=4)
    g.add_arc(1, 3, 10, cost=1)
    g.add_arc(2, 3, 10, cost=3)
    g.add_arc(3, 4, 10, cost=1)
    g.add_arc(1, 2, 5,  cost=1)

    assert_no_negative_cycle(g)

    flow, cost = min_cost_flow_dijkstra(g, source, sink)
    print(f"Flot total : {flow}")
    print(f"Coût total : {cost}")
    print(f"(attendu : flow=10, cost=40)")


def demo_comparison_bf_vs_dijkstra():
    """
    Comparaison Bellman-Ford et Dijkstra sur le même graphe.
    Les deux algorithmes doivent produire des résultats identiques.
    """
    print("\n" + "=" * 60)
    print("DEMO 5 : Comparaison Bellman-Ford vs Dijkstra")
    print("=" * 60)

    def make_graph():
        g = ResidualGraph(6)
        g.add_arc(0, 1, 8, cost=3)
        g.add_arc(0, 2, 6, cost=1)
        g.add_arc(1, 3, 5, cost=2)
        g.add_arc(2, 3, 4, cost=4)
        g.add_arc(2, 4, 5, cost=2)
        g.add_arc(3, 5, 7, cost=1)
        g.add_arc(4, 5, 6, cost=3)
        g.add_arc(1, 4, 3, cost=1)
        return g

    g1 = make_graph()
    g2 = make_graph()

    flow_bf, cost_bf = min_cost_flow_bellman_ford(g1, 0, 5)
    flow_dj, cost_dj = min_cost_flow_dijkstra(g2, 0, 5)

    print(f"Bellman-Ford : flow={flow_bf}, cost={cost_bf}")
    print(f"Dijkstra     : flow={flow_dj}, cost={cost_dj}")

    if flow_bf == flow_dj and cost_bf == cost_dj:
        print("✓ Résultats identiques")
    else:
        print("✗ DIVERGENCE !")


def demo_negative_cycle_detection():
    """
    Détection de cycles négatifs sur trois graphes distincts.
    """
    print("\n" + "=" * 60)
    print("DEMO 6 : Détection de Cycles Négatifs")
    print("=" * 60)

    # Cycle 0→1→2→0 de coût 2+3-4 = +1 : pas de cycle négatif
    g1 = ResidualGraph(4)
    g1.add_arc(0, 1, 10, cost=2)
    g1.add_arc(1, 2, 10, cost=3)
    g1.add_arc(2, 0, 10, cost=-4)
    g1.add_arc(0, 3, 10, cost=1)

    has_cycle1, _ = detect_negative_cycle(g1)
    print(f"\nGraphe 1 (cycle de coût +1) : cycle négatif = {has_cycle1}  (attendu : False)")

    # Cycle 0→1→2→0 de coût 1+1-5 = -3 : cycle négatif
    g2 = ResidualGraph(3)
    g2.add_arc(0, 1, 10, cost=1)
    g2.add_arc(1, 2, 10, cost=1)
    g2.add_arc(2, 0, 10, cost=-5)

    has_cycle2, cycle2 = detect_negative_cycle(g2)
    print(f"\nGraphe 2 (cycle de coût -3) : cycle négatif = {has_cycle2}  (attendu : True)")
    if cycle2:
        print(f"  Nœuds du cycle : {cycle2}")

    # Cycle 1→2→3→1 de coût 3-8+2 = -3 dans un graphe plus grand
    g3 = ResidualGraph(5)
    g3.add_arc(0, 1, 10, cost=2)
    g3.add_arc(1, 2, 10, cost=3)
    g3.add_arc(2, 3, 10, cost=-8)
    g3.add_arc(3, 1, 10, cost=2)
    g3.add_arc(0, 4, 10, cost=1)

    has_cycle3, cycle3 = detect_negative_cycle(g3)
    print(f"\nGraphe 3 (cycle 1→2→3→1, coût=-3) : cycle négatif = {has_cycle3}  (attendu : True)")
    if cycle3:
        print(f"  Nœuds du cycle : {cycle3}")


if __name__ == "__main__":
    demo_ford_fulkerson()
    demo_assignment_graph()
    demo_min_cost_flow_bellman_ford()
    demo_min_cost_flow_dijkstra()
    demo_comparison_bf_vs_dijkstra()
    demo_negative_cycle_detection()
    print("\n" + "=" * 60)
    print("✓ Toutes les démonstrations terminées avec succès.")
    print("=" * 60)
