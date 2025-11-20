"""
TSP Approximation Algorithm

This module implements the 2-approximation algorithm for Metric TSP.
It constructs a Minimum Spanning Tree (MST) using Prim's algorithm and then
performs a preorder Depth-First Search (DFS) traversal to create the tour.
"""

import sys
from tsp_utils import euclidean_distance, calculate_tour_distance

# Increase recursion depth for deep DFS traversals on large instances
sys.setrecursionlimit(20000)


def solve_tsp(coordinates, cutoff_time=None):
    """
    Solve TSP using MST approximation algorithm.
    
    Args:
        coordinates: Dictionary mapping vertex_id -> (x, y)
        cutoff_time: Ignored for this algorithm (runs fast enough)
        
    Returns:
        tuple: (tour, total_distance)
    """
    if not coordinates:
        return [], 0.0
        
    vertices = sorted(coordinates.keys())
    n = len(vertices)
    
    if n == 1:
        return vertices, 0.0
        
    # Map vertex ID to index (0 to n-1) for easier array handling
    id_to_idx = {v_id: i for i, v_id in enumerate(vertices)}
    idx_to_id = {i: v_id for i, v_id in enumerate(vertices)}
    
    # 1. MST-Prim Algorithm
    # Start from root vertex (first vertex in sorted list)
    root_idx = 0
    
    parent = [None] * n
    key = [float('inf')] * n
    in_mst = [False] * n
    
    key[root_idx] = 0
    
    for _ in range(n):
        # Find vertex u not in MST with minimum key value
        u_idx = -1
        min_val = float('inf')
        
        for i in range(n):
            if not in_mst[i] and key[i] < min_val:
                min_val = key[i]
                u_idx = i
        
        if u_idx == -1:
            break
            
        in_mst[u_idx] = True
        
        # Update key values of adjacent vertices
        # Since graph is complete, all other vertices are adjacent
        u_coord = coordinates[idx_to_id[u_idx]]
        
        for v_idx in range(n):
            if not in_mst[v_idx]:
                v_coord = coordinates[idx_to_id[v_idx]]
                weight = euclidean_distance(u_coord, v_coord)
                
                if weight < key[v_idx]:
                    key[v_idx] = weight
                    parent[v_idx] = u_idx

    # Build MST adjacency list for DFS
    mst_adj = {i: [] for i in range(n)}
    for i in range(1, n):  # Skip root which has no parent
        p = parent[i]
        if p is not None:
            mst_adj[p].append(i)
            mst_adj[i].append(p)
            
    # Sort children for deterministic traversal (optional but good practice)
    for i in range(n):
        mst_adj[i].sort()

    # 2. Preorder DFS Traversal
    tour_indices = []
    visited = [False] * n
    
    def dfs(u):
        visited[u] = True
        tour_indices.append(u)
        
        for v in mst_adj[u]:
            if not visited[v]:
                dfs(v)
    
    dfs(root_idx)
    
    # Convert indices back to vertex IDs
    tour = [idx_to_id[i] for i in tour_indices]
    
    # 3. Calculate Tour Distance
    total_distance = calculate_tour_distance(tour, coordinates)
    
    return tour, total_distance

