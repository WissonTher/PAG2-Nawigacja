from algorithms.djikstra import djikstra
from algorithms.a_star import a_star

class Graph:
    def __init__(self, nodes, edges):
        n_len = len(nodes)
        self.links = [[0] * n_len for _ in range(n_len)]
        self.n_len = n_len
        self.nodes = [''] * n_len
        self.positions = {}
        self.adj = [[] for _ in range(n_len)]

        for e, (u, v, w) in edges.items():
            self.links[u][v] = w
            self.links[v][u] = w
            self.adj[u].append([v, w])
            self.adj[v].append([u, w])
        for node, node_d in nodes.items():
            self.nodes[node] = node

    def __str__(self):
        s = "nodes:\n"
        for i, w in enumerate(self.nodes):
            s += f"{i}: {w}\n"

        s += "\nedges:\n"
        for u in range(self.n_len):
            for v in range(self.n_len):
                w = self.links[u][v]
                if w != 0:
                    s += f"{u} -> {v} [{w:.2f}]\n"
        return s

    def a_star(self, start, target, return_cost = False):
        return a_star(self, start, target, return_cost)

    def djikstra(self, start, target=None):
        return djikstra(self, start, target)