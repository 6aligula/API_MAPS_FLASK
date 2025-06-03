import numpy as np
import math
from sklearn.cluster import DBSCAN
from datetime import datetime
from typing import List
from ..schemas.route import RoutePoint

def filter_route_points_ml(points: List[RoutePoint], start_date: datetime, end_date: datetime, 
                           radius_km: float = 0.5, min_samples: int = 2) -> List[RoutePoint]:
    # Filtrar puntos por fecha
    filtered_points = [pt for pt in points if start_date <= pt.timestamp <= end_date]
    if not filtered_points:
        return []
    
    # Convertir coordenadas a radianes
    coords = np.array([[math.radians(pt.lat), math.radians(pt.lon)] for pt in filtered_points])
    eps = radius_km / 6371.0  # Conversión km -> radianes

    db = DBSCAN(eps=eps, min_samples=min_samples, metric='haversine')
    clusters = db.fit_predict(coords)
    
    # Seleccionar puntos que NO sean ruido (-1)
    coherent_points = [pt for pt, label in zip(filtered_points, clusters) if label != -1]
    coherent_points.sort(key=lambda pt: pt.timestamp)
    
    return coherent_points