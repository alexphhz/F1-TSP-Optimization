import numpy as np
import pandas as pd
from .haversine import haversine

def calculate_distance_matrix(df: pd.DataFrame) -> np.ndarray:
    """Build full distance matrix (miles) from DataFrame with ['Latitude','Longitude']."""
    n = len(df)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                matrix[i, j] = haversine(df.iloc[i]['Latitude'], df.iloc[i]['Longitude'],
                                         df.iloc[j]['Latitude'], df.iloc[j]['Longitude'])
    return matrix
