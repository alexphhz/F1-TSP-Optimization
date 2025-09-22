import numpy as np
from itertools import permutations

def brute_force_tsp(distance_matrix: np.ndarray):
    """Solve TSP by brute force (only for very small n). Returns (route, distance)."""
    n = len(distance_matrix)
    best_route, best_distance = None, float("inf")
    for perm in permutations(range(n)):
        total = sum(distance_matrix[perm[i], perm[(i + 1) % n]] for i in range(n))
        if total < best_distance:
            best_distance = total
            best_route = list(perm)
    return best_route, best_distance
