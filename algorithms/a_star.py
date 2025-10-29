import math
import heapq

def heuristics(graph, a, b):
    if a in graph.positions and b in graph.positions:
        (x1, y1) = graph.positions[a]
        (x2, y2) = graph.positions[b]
        return math.hypot(x1 - x2, y1 - y2)
    return 0

def a_star(graph, start, target, return_cost=False):
    start_id = graph.nodes.index(start)
    target_id = graph.nodes.index(target)

    g = [float('inf')] * graph.n_len
    f = [float('inf')] * graph.n_len
    g[start_id] = 0
    f[start_id] = heuristics(graph, start, target)

    Q = []
    heapq.heappush(Q, (f[start_id], start_id))
    came_from = {}
    S = set()

    while Q:
        _, u = heapq.heappop(Q)
        if u in S:
            continue
        S.add(u)

        if u == target_id:
            path = [graph.nodes[u]]
            while u in came_from:
                u = came_from[u]
                path.append(graph.nodes[u])
            path = path[::-1]
            if return_cost:
                return path, g[target_id]
            return path
        
        for v in range(graph.n_len):
            w = graph.links[u][v]
            if w == 0 or v in S:
                continue

            temp_g = g[u] + w
            if temp_g < g[v]:
                came_from[v] = u
                g[v] = temp_g
                f[v] = temp_g + heuristics(
                    graph,
                    graph.nodes[v],
                    graph.nodes[target_id]
                )
                heapq.heappush(Q, (f[v], v))
    
    if return_cost:
        return None, float('inf')
    return None
