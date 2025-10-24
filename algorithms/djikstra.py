def djikstra(graph, start, target=None):
    start_id = graph.wierzcholki.index(start)
    target_id = graph.wierzcholki.index(target) if target is not None else None
    n = graph.lenkr
    lens = [float('inf')] * n
    lens[start_id] = 0.0
    S = [False] * n
    pre = [-1] * n

    for _ in range(n):
        minlen = float('inf')
        u = None
        for i in range(n):
            if not S[i] and lens[i] < minlen:
                minlen = lens[i]
                u = i

        if u is None or lens[u] == float('inf'):
            break

        S[u] = True

        if target_id is not None and u == target_id:
            path_nodes = []
            current = u
            while current != -1:
                path_nodes.append(current)
                if current == start_id:
                    break
                current = pre[current]
            if not path_nodes or path_nodes[-1] != start_id:
                return [], float('inf')
            path_nodes.reverse()
            path = [graph.wierzcholki[i] for i in path_nodes]
            return path, lens[u]

        for v in range(n):
            w = graph.polaczenia[u][v]
            if w != 0 and not S[v]:
                alt = lens[u] + w
                if alt < lens[v]:
                    lens[v] = alt
                    pre[v] = u

    if target_id is not None:
        if lens[target_id] == float('inf'):
            return [], float('inf')
        path_nodes = []
        current = target_id
        while current != -1:
            path_nodes.append(current)
            if current == start_id:
                break
            current = pre[current]
        if not path_nodes or path_nodes[-1] != start_id:
            return [], float('inf')
        path_nodes.reverse()
        path = [graph.wierzcholki[i] for i in path_nodes]
        return path, lens[target_id]
    return lens