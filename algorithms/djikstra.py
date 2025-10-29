import heapq
def djikstra(graph, start, target = None):
    n = graph.n_len
    inf = float('inf')
    lens = [inf] * n
    lens[start] = 0.0
    S = [False] * n
    pre = [-1] * n

    heap = [(0.0, start)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > lens[u] or S[u]:
            continue

        S[u] = True
        if target is not None and u == target:
            break

        for v, w in graph.adj[u]:
            if S[v]:
                continue
            alt = d + w
            if alt < lens[v]:
                lens[v] = alt
                pre[v] = u
                heapq.heappush(heap, (alt, v))

    if target is not None:
        if lens[target] == inf:
            return None, inf
        path = []
        current = target
        while current != -1:
            path.append(current)
            if current == start:
                break
            current = pre[current]
        if not path or path[-1] != start:
            return None, inf
        path.reverse()
        return path, lens[target]
    else:
        paths = []
        for targ in range(n):
            if lens[targ] == inf:
                paths.append(None)
                continue
            path = []
            current = targ
            while current != -1:
                path.append(current)
                if current == start:
                    break
                current = pre[current]
            if not path or path[-1] != start:
                paths.append(None)
            else:
                path.reverse()
                paths.append(path)
        return paths, lens