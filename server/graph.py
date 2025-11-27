from algorithms.djikstra import djikstra
from algorithms.a_star import a_star
from typing import List, Tuple
class Graph:
    def __init__(self, nodes, adj):
        n_len = len(nodes)
        self.n_len = n_len
        self.nodes = nodes.items()
        self.positions = {}
        self.adj: List[List[Tuple[int, float, int]]] = adj

    def __str__(self):
        s = "nodes:\n"
        for i, w in enumerate(self.nodes):
            s += f"{i}: {w}\n"

        s += "\nedges:\n"
        for u in range(self.n_len):
            for v in range(self.n_len):
                w = self.adj[u][v]
                if w != 0:
                    s += f"{u} -> {v} [{w:.2f}]\n"
        return s

    def a_star(self, start, target, return_cost = False):
        return a_star(self, start, target, return_cost)

    def djikstra(self, start, target=None, max_cost=None):
        return djikstra(self, start, target, max_cost)