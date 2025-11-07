import heapq
def djikstra(graph, start, target=None):
    n = graph.n_len
    inf = float('inf')
    lens = [inf] * n
    lens[start] = 0.0
    S = bytearray(n)
    pre = [-1] * n
    preedge = [-1] * n

    adj = graph.adj
    heappush = heapq.heappush
    heappop = heapq.heappop

    heap = [(0.0, start)]

    if target is not None:
        while heap:
            d, u = heappop(heap)
            if S[u] or d != lens[u]:
                continue
            S[u] = 1
            if u == target:
                break
            for v, w, e in adj[u]:
                if S[v]:
                    continue
                alt = d + w
                if alt < lens[v]:
                    lens[v] = alt
                    pre[v] = u
                    preedge[v] = e
                    heappush(heap, (alt, v))

        if lens[target] == inf:
            return inf, None, None

        path = []
        edges = []
        cur = target
        while cur != -1:
            path.append(cur)
            if cur == start:
                break
            edges.append(preedge[cur])
            cur = pre[cur]
        if not path or path[-1] != start:
            return inf, None, None
        path.reverse()
        edges.reverse()
        return lens[target], path, edges

    while heap:
        d, u = heappop(heap)
        if S[u] or d != lens[u]:
            continue
        S[u] = 1
        for v, w, e in adj[u]:
            if S[v]:
                continue
            alt = d + w
            if alt < lens[v]:
                lens[v] = alt
                pre[v] = u
                preedge[v] = e
                heappush(heap, (alt, v))

    paths = [None] * n
    alledges = [None] * n

    if lens[start] != inf:
        connections = [[] for _ in range(n)]
        for v in range(n):
            p = pre[v]
            if p != -1:
                connections[p].append(v)

        stack = [(start, 0)]
        path = []
        edges = []

        while stack:
            u, idx = stack[-1]
            if idx == 0:
                path.append(u)
                paths[u] = list(path)
                alledges[u] = [] if u == start else list(edges)

            if idx < len(connections[u]):
                connect = connections[u][idx]
                stack[-1] = (u, idx + 1)
                edges.append(preedge[connect])
                stack.append((connect, 0))
            else:
                stack.pop()
                finished = path.pop()
                if finished != start and edges:
                    edges.pop()

    return lens, paths, alledges