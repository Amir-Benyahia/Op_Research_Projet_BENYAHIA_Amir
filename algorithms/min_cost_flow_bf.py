# Min cost flow par chemins augmentants successifs - version Bellman-Ford
# bellman-ford classique, voir cours slide 1.55
# complexite O(n^2 * m)

from graph.residual_graph import ResidualGraph  # noqa: F401
from algorithms.negative_cycle import detect_negative_cycle


def bellman_ford_shortest_path(graph, source, sink):
    """Plus court chemin source->sink avec Bellman-Ford."""
    INF = float('inf')
    dist = {node: INF for node in graph.adj}
    pred = {node: None for node in graph.adj}
    dist[source] = 0

    n = graph.num_nodes

    # n-1 iterations de relaxation
    for _ in range(n - 1):
        updated = False
        for node in graph.adj:
            if dist[node] == INF:
                continue
            for arc in graph.adj[node]:
                if arc.capacity > 0:
                    new_dist = dist[node] + arc.cost
                    if new_dist < dist[arc.dst]:
                        dist[arc.dst] = new_dist
                        pred[arc.dst] = arc
                        updated = True
        if not updated:
            break

    # check cycle negatif - si on peut encore relaxer c'est mort
    for node in graph.adj:
        if dist[node] == INF:
            continue
        for arc in graph.adj[node]:
            if arc.capacity > 0 and dist[node] + arc.cost < dist[arc.dst]:
                return None, None

    if dist[sink] == INF:
        return None, None

    return dist, pred


def reconstruct_path(pred, source, sink):
    path = []
    current = sink
    while current != source:
        arc = pred[current]
        if arc is None:
            return None
        path.append(arc)
        current = arc.src
    path.reverse()
    return path


def min_cost_flow_bellman_ford(graph, source, sink, required_flow=None):
    """Calcule le flot de cout min de source vers sink. Retourne (flow, cost)."""
    total_flow = 0
    total_cost = 0

    while True:
        if required_flow is not None and total_flow >= required_flow:
            break

        # safety check : pas de cycle negatif dans le residuel
        has_neg_cycle, cycle = detect_negative_cycle(graph)
        if has_neg_cycle:
            raise RuntimeError(f"Cycle négatif détecté dans le graphe résiduel : {cycle}")

        dist, pred = bellman_ford_shortest_path(graph, source, sink)
        if dist is None:
            break

        path = reconstruct_path(pred, source, sink)
        if path is None:
            break

        # calcul du bottleneck
        delta = min(arc.capacity for arc in path)
        if required_flow is not None:
            delta = min(delta, required_flow - total_flow)

        path_cost = sum(arc.cost for arc in path)

        graph.augment(path, delta)
        total_flow += delta
        total_cost += path_cost * delta

    return total_flow, total_cost
