def djikstra(graph, start, target=None):
    start_id = graph.wierzcholki.index(start)
    lens = [float('inf')] * graph.lenkr
    lens[start_id] = 0
    S = [False] * graph.lenkr

    for _ in range(graph.lenkr):
        minlen = float('inf')
        u = None
        for i in range(graph.lenkr):
            if not S[i] and lens[i] < minlen:
                minlen = lens[i]
                u = i

        if u is None:
            break

        S[u] = True
        for v in range(graph.lenkr):
            if graph.polaczenia[u][v] != 0 and not S[v]:
                alt = lens[u] + graph.polaczenia[u][v]
                if alt < lens[v]:
                    lens[v] = alt
        if target is not None and u == graph.wierzcholki.index(target):
            return lens[u]
    if target is not None:
        return float('inf')
    return len
