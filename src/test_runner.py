"""Quick smoke test: builds matrix, runs nearest neighbor, prints distance."""
# Supports both:
#   python -m src.test_runner   (recommended, from project root)
#   python src/test_runner.py   (fallback; adds parent to sys.path)

try:
    from .calculate_matrix import calculate_distance_matrix
    from .tsp_heuristic import nearest_neighbor
except ImportError:
    import os, sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.calculate_matrix import calculate_distance_matrix
    from src.tsp_heuristic import nearest_neighbor

import pandas as pd

if __name__ == "__main__":
    df = pd.read_excel("data/f1_tracks.xlsx")
    dist = calculate_distance_matrix(df)
    path, miles = nearest_neighbor(dist, start_index=0)
    cities = [df.iloc[i]["City"] for i in path]
    print("Route:", " -> ".join(cities))
    print("Total miles:", round(miles, 2))
