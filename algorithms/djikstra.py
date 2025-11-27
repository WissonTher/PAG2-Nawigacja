import heapq
def djikstra(graph, start, target=None, max_cost=None):
    n = graph.n_len
    inf = float('inf')
    lens = [inf] * n
    lens[start] = 0.0
    S = bytearray(n)
    pre = [-1] * n

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
            for v, _, w in adj[u]:
                if S[v]:
                    continue
                alt = d + w
                if alt < lens[v]:
                    lens[v] = alt
                    pre[v] = u
                    heappush(heap, (alt, v))

        if lens[target] == inf:
            return -1, None, None

        path = []
        cur = target
        while cur != -1:
            path.append(cur)
            if cur == start:
                break
            cur = pre[cur]
        if not path or path[-1] != start:
            return -1, None, None
        path.reverse()
        return lens[target], path

    while heap:
        d, u = heappop(heap)
        if S[u] or d != lens[u]:
            continue
        S[u] = 1
        for v, _, w in adj[u]:
            if S[v]:
                continue
            alt = d + w
            if alt < lens[v] and (max_cost is None or alt <= max_cost):
                lens[v] = alt
                pre[v] = u
                heappush(heap, (alt, v))

    paths = [None] * n

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

            if idx < len(connections[u]):
                connect = connections[u][idx]
                stack[-1] = (u, idx + 1)
                stack.append((connect, 0))
            else:
                stack.pop()
                finished = path.pop()
                if finished != start and edges:
                    edges.pop()

    return [x for x in lens if x != inf and x > 0], paths