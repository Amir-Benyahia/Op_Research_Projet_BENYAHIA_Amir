class Arc:
    def __init__(self, src, dst, capacity, cost=0, lower=0):
        self.src = src
        self.dst = dst
        self.capacity = capacity
        self.cost = cost
        self.lower = lower
        self.flow = 0
        self.reverse = None


class ResidualGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.adj = {i: [] for i in range(num_nodes)}

    def add_arc(self, src, dst, capacity, cost=0, lower=0):
        forward = Arc(src, dst, capacity - lower, cost, lower)
        backward = Arc(dst, src, 0, -cost, 0)
        forward.reverse = backward
        backward.reverse = forward
        self.adj[src].append(forward)
        self.adj[dst].append(backward)
        return forward

    def augment(self, path_arcs, flow_amount):
        for arc in path_arcs:
            arc.capacity -= flow_amount
            arc.reverse.capacity += flow_amount
            arc.flow += flow_amount
            arc.reverse.flow -= flow_amount
