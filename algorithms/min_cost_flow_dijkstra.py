"""
Min Cost Flow par chemins augmentants successifs les moins chers — variante Dijkstra.

Dijkstra est plus rapide que Bellman-Ford (O((V+E) log V) vs O(VE)), mais il
n'accepte pas les coûts négatifs. On utilise la renormalisation de Johnson :

    coût réduit : c_R(u,v) = h[u] + c(u,v) - h[v]

Si h[v] contient les distances actuelles depuis la source, alors c_R(u,v) >= 0
pour tout arc résiduel, et Dijkstra peut s'appliquer.

Après chaque augmentation, les potentiels sont mis à jour (h[v] += dist[v]),
ce qui préserve l'invariant c_R >= 0 pour l'itération suivante.

Complexité : O(n * (V+E) log V)
"""

import heapq
from graph.residual_graph import ResidualGraph
from algorithms.negative_cycle import detect_negative_cycle


def initialize_potentials_bellman_ford(graph, source):
    """
    Initialise les potentiels h via Bellman-Ford (exécuté une seule fois).

    Nécessaire au départ car le graphe peut contenir des arcs de coût négatif.
    Une fois les potentiels initialisés, Dijkstra est utilisable à chaque itération.

    Les nœuds inatteignables reçoivent le potentiel 0 par convention.

    Retourne : dict {node → h[node]}
    """
    INF = float('inf')
    h = {node: INF for node in graph.adj}
    h[source] = 0

    n = graph.num_nodes
    for _ in range(n - 1):
        updated = False
        for node in graph.adj:
            if h[node] == INF:
                continue
            for arc in graph.adj[node]:
                if arc.capacity > 0 and h[node] + arc.cost < h[arc.dst]:
                    h[arc.dst] = h[node] + arc.cost
                    updated = True
        if not updated:
            break

    for node in h:
        if h[node] == INF:
            h[node] = 0

    return h


def dijkstra_with_potentials(graph, source, potentials):
    """
    Dijkstra avec coûts réduits c_R(u,v) = h[u] + c(u,v) - h[v].

    Les coûts réduits sont toujours >= 0 si les potentiels sont à jour,
    ce qui garantit la validité de Dijkstra.

    Retourne :
        dist — dict {node → distance réduite depuis source}
        pred — dict {node → arc utilisé pour atteindre ce nœud}
    """
    INF = float('inf')
    dist = {node: INF for node in graph.adj}
    pred = {node: None for node in graph.adj}
    dist[source] = 0

    heap = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)

        if d > dist[node]:
            continue  # entrée obsolète dans le tas

        for arc in graph.adj[node]:
            if arc.capacity <= 0:
                continue

            reduced_cost = potentials[arc.src] + arc.cost - potentials[arc.dst]

            if reduced_cost < -1e-9:
                raise RuntimeError(
                    f"Coût réduit négatif sur arc ({arc.src},{arc.dst}) : "
                    f"{reduced_cost:.6f} — potentiels invalides."
                )

            effective_cost = max(0.0, reduced_cost)  # clamp pour erreurs numériques
            new_dist = dist[node] + effective_cost

            if new_dist < dist[arc.dst]:
                dist[arc.dst] = new_dist
                pred[arc.dst] = arc
                heapq.heappush(heap, (new_dist, arc.dst))

    return dist, pred


def min_cost_flow_dijkstra(graph, source, sink, required_flow=None):
    """
    Calcule le flot de coût minimum de source vers sink (variante Dijkstra).

    Paramètres :
        graph         — ResidualGraph configuré
        source        — nœud source
        sink          — nœud puits
        required_flow — flot exact à envoyer (None = maximum possible)

    Retourne :
        (total_flow, total_cost)
    """
    total_flow = 0
    total_cost = 0

    has_neg_cycle, cycle = detect_negative_cycle(graph)
    if has_neg_cycle:
        raise RuntimeError(f"Cycle négatif dans le graphe initial : {cycle}")

    # Bellman-Ford une seule fois pour initialiser les potentiels
    potentials = initialize_potentials_bellman_ford(graph, source)

    while True:
        if required_flow is not None and total_flow >= required_flow:
            break

        dist, pred = dijkstra_with_potentials(graph, source, potentials)

        if dist[sink] == float('inf'):
            break

        # Reconstruction du chemin source→sink
        path_arcs = []
        current = sink
        while current != source:
            arc = pred[current]
            if arc is None:
                break
            path_arcs.append(arc)
            current = arc.src
        path_arcs.reverse()

        if not path_arcs:
            break

        bottleneck = min(arc.capacity for arc in path_arcs)
        if required_flow is not None:
            bottleneck = min(bottleneck, required_flow - total_flow)

        # Coût réel du chemin (coûts originaux, pas les coûts réduits)
        real_path_cost = sum(arc.cost for arc in path_arcs)

        graph.augment(path_arcs, bottleneck)
        total_flow += bottleneck
        total_cost += real_path_cost * bottleneck

        # Mise à jour des potentiels : préserve c_R >= 0 à l'itération suivante
        for node in graph.adj:
            if dist[node] < float('inf'):
                potentials[node] += dist[node]

    return total_flow, total_cost
