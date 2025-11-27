import math
import heapq

def heuristics(graph, a, b):
    if a in graph.positions and b in graph.positions:
        (x1, y1) = graph.positions[a]
        (x2, y2) = graph.positions[b]
        return math.hypot(x1 - x2, y1 - y2)
    return 0

def a_star(graph, start, target, return_cost=True):
    nodes = [item[0] for item in graph.nodes]
    start_id = nodes.index(start) 
    target_id = nodes.index(target)
    
    g = [float('inf')] * graph.n_len
    dist = [float('inf')] * graph.n_len
    f = [float('inf')] * graph.n_len 
    g[start_id] = 0
    dist[start_id] = 0
    f[start_id] = heuristics(graph, start, target) 

    Q = []
    heapq.heappush(Q, (f[start_id], start_id))
    came_from = {} 
    origin_id = {}
    S = set() 

    while Q:
        _, u = heapq.heappop(Q) 
        if u in S:
            continue
        S.add(u)

        if u == target_id:
            path = [nodes[u]]
            origin = []
            while u in came_from:
                origin.append(origin_id[u])
                u = came_from[u]
                path.append(nodes[u])
            path = path[::-1]
            origin = origin[::-1]
            if return_cost:
                return path, g[target_id], dist[target_id], origin
            return path, origin
        
        for neighbor_data in graph.adj[u]:
            v = neighbor_data[0]
            d = neighbor_data[1]
            w = neighbor_data[2] 
            e = neighbor_data[3]
            
            if v in S: 
                continue

            temp_g = g[u] + w 
            temp_d = dist[u] + d
            
            if temp_g < g[v]:
                came_from[v] = u
                origin_id[v] = e
                g[v] = temp_g
                dist[v] = temp_d
                
                v = nodes[v]
                f[v] = temp_g + heuristics(graph, v, target)
                
                heapq.heappush(Q, (f[v], v))
    
    if return_cost:
        return None, float('inf'), float('inf'), []
    return None, []