from algorithms.djikstra import djikstra
from algorithms.a_star import a_star

class Graph:
    def __init__(self, wierzcholki, krawedzie):
        lenkr = len(wierzcholki)
        self.polaczenia = [[0] * lenkr for _ in range(lenkr)]
        self.lenkr = lenkr
        self.wierzcholki = [''] * lenkr
        self.positions = {}

        for k, kraw in krawedzie.items():
            u = krawedzie[k][0]
            v = krawedzie[k][1]
            waga = krawedzie[k][2]
            self.polaczenia[u][v] = waga
            self.polaczenia[v][u] = waga
        for w, wier in wierzcholki.items():
            self.wierzcholki[w] = w

    def __str__(self):
        s = "Wierzcholki:\n"
        for i, w in enumerate(self.wierzcholki):
            s += f"{i}: {w}\n"

        s += "\nKrawedzie:\n"
        for u in range(self.lenkr):
            for v in range(self.lenkr):
                waga = self.polaczenia[u][v]
                if waga != 0:
                    s += f"{u} -> {v} [{waga:.2f}]\n"
        return s

    def a_star(self, start, target, return_cost = False):
        return a_star(self, start, target, return_cost)

    def djikstra(self, start, target=None):
        return djikstra(self, start, target)