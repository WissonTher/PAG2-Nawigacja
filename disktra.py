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

    def dijkstra(self, poczatkowy, koncowy=None):
        poczatkowy_id = self.wierzcholki.index(poczatkowy)
        odl = [float('inf')] * self.lenkr
        odl[poczatkowy_id] = 0
        S = [False] * self.lenkr

        for _ in range(self.lenkr):
            minodl = float('inf')
            u = None
            for i in range(self.lenkr):
                if not S[i] and odl[i] < minodl:
                    minodl = odl[i]
                    u = i

            if u is None:
                break
                
            S[u] = True
            for v in range(self.lenkr):
                if self.polaczenia[u][v] != 0 and not S[v]:
                    alt = odl[u] + self.polaczenia[u][v]
                    if alt < odl[v]:
                        odl[v] = alt
             if koncowy is not None and u == self.wierzcholki.index(koncowy):
                return odl[u]
        if koncowy is not None:
            return float('inf')
        return odl

