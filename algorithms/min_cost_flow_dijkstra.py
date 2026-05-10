# Min cost flow avec Dijkstra + renormalisation des couts (Johnson reweighting)
# cout reduit : c_R(u,v) = h[u] + c(u,v) - h[v]   -> toujours >= 0

import heapq
from graph.residual_graph import ResidualGraph  # noqa: F401
from algorithms.negative_cycle import detect_negative_cycle


def initialize_potentials_bellman_ford(graph, source):
    """Init des potentiels h via Bellman-Ford (une seule fois au depart)."""
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

    # noeuds inatteignables : on met 0 par convention
    for node in h:
        if h[node] == INF:
            h[node] = 0

    return h


def dijkstra_with_potentials(graph, source, h):
    """Dijkstra avec couts reduits."""
    INF = float('inf')
    dist = {node: INF for node in graph.adj}
    pred = {node: None for node in graph.adj}
    dist[source] = 0

    heap = [(0, source)]

    while heap:
        d, node = heapq.heappop(heap)

        if d > dist[node]:
            continue  # entree obsolete

        for arc in graph.adj[node]:
            if arc.capacity <= 0:
                continue

            # cout reduit
            reduced_cost = h[arc.src] + arc.cost - h[arc.dst]

            if reduced_cost < -1e-9:
                # ca ne devrait jamais arriver si les potentiels sont bons
                raise RuntimeError(
                    f"Coût réduit négatif sur arc ({arc.src},{arc.dst}) : "
                    f"{reduced_cost:.6f} — potentiels invalides."
                )

            # clamp pour erreurs numeriques
            effective_cost = max(0.0, reduced_cost)
            new_dist = dist[node] + effective_cost

            if new_dist < dist[arc.dst]:
                dist[arc.dst] = new_dist
                pred[arc.dst] = arc
                heapq.heappush(heap, (new_dist, arc.dst))

    return dist, pred


def min_cost_flow_dijkstra(graph, source, sink, required_flow=None):
    """Min cost flow version Dijkstra."""
    total_flow = 0
    total_cost = 0

    # check initial : pas de cycle negatif au depart
    has_neg_cycle, cycle = detect_negative_cycle(graph)
    if has_neg_cycle:
        raise RuntimeError(f"Cycle négatif dans le graphe initial : {cycle}")

    # Bellman-Ford une seule fois pour les potentiels initiaux
    h = initialize_potentials_bellman_ford(graph, source)

    while True:
        if required_flow is not None and total_flow >= required_flow:
            break

        dist, pred = dijkstra_with_potentials(graph, source, h)

        if dist[sink] == float('inf'):
            break

        # reconstruction du chemin
        path = []
        current = sink
        while current != source:
            arc = pred[current]
            if arc is None:
                break
            path.append(arc)
            current = arc.src
        path.reverse()

        if not path:
            break

        delta = min(arc.capacity for arc in path)
        if required_flow is not None:
            delta = min(delta, required_flow - total_flow)

        # cout reel (couts originaux, pas les reduits)
        real_path_cost = sum(arc.cost for arc in path)

        graph.augment(path, delta)
        total_flow += delta
        total_cost += real_path_cost * delta

        # update des potentiels : h[v] += dist[v]
        # ca preserve c_R >= 0 pour la prochaine iteration
        for node in graph.adj:
            if dist[node] < float('inf'):
                h[node] += dist[node]

    return total_flow, total_cost
