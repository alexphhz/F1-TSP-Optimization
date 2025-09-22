import numpy as np
import pandas as pd
from .calculate_matrix import calculate_distance_matrix

def nearest_neighbor(matrix: np.ndarray, start_index: int = 0):
    n = matrix.shape[0]
    visited = {start_index}
    path = [start_index]
    total_distance = 0.0
    while len(visited) < n:
        last = path[-1]
        next_city = int(np.argmin([matrix[last][j] if j not in visited else np.inf for j in range(n)]))
        path.append(next_city)
        visited.add(next_city)
        total_distance += matrix[last][next_city]
    total_distance += matrix[path[-1]][path[0]]
    path.append(start_index)  # complete cycle
    return path, total_distance
