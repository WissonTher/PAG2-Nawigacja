class Graph:
    def __init__(self, wierzcholki, krawedzie):
        lenkr = len(wierzcholki)
        self.polaczenia = [[0] * lenkr for _ in range(lenkr)]
        self.lenkr = lenkr
        self.wierzcholki = [''] * lenkr
        for k, kraw in krawedzie.items():
            u = krawedzie[k][0]
            v = krawedzie[k][1]
            waga = krawedzie[k][2]
            self.polaczenia[u][v] = waga
            self.polaczenia[v][u] = waga
        for w, wier in wierzcholki.items():
            self.wierzcholki[w] = w


    def dijkstra(self, wyjsciowy):
        wyjsciowy_id = self.wierzcholki.index(wyjsciowy)
        Q = [float('inf')] * self.lenkr
        Q[wyjsciowy_id] = 0
        S = [False] * self.lenkr

        for _ in range(self.lenkr):
            minodl = float('inf')
            u = None
            for i in range(self.lenkr):
                if not S[i] and Q[i] < minodl:
                    minodl = Q[i]
                    u = i

            if u is None:
                break

            S[u] = True

            for v in range(self.lenkr):
                if self.polaczenia[u][v] != 0 and not S[v]:
                    alt = Q[u] + self.polaczenia[u][v]
                    if alt < Q[v]:
                        Q[v] = alt

        return Q

