import requests
from datetime import datetime, timedelta
import json

# URL base de tu API
BASE_URL = "https://senderos-gps-312503514287.europe-west1.run.app"

# Ruta 1: Sendero Madrid - Casa de Campo
route1 = {
    "device_id": "device_madrid_001",
    "points": [
        {"lat": 40.4168, "lon": -3.7038, "timestamp": "2024-01-15T09:00:00Z", "accuracy": 5.0, "altitude": 650.0},
        {"lat": 40.4170, "lon": -3.7040, "timestamp": "2024-01-15T09:05:00Z", "accuracy": 4.5, "altitude": 655.0},
        {"lat": 40.4175, "lon": -3.7045, "timestamp": "2024-01-15T09:10:00Z", "accuracy": 3.8, "altitude": 660.0},
        {"lat": 40.4180, "lon": -3.7050, "timestamp": "2024-01-15T09:15:00Z", "accuracy": 4.2, "altitude": 665.0},
        {"lat": 40.4185, "lon": -3.7055, "timestamp": "2024-01-15T09:20:00Z", "accuracy": 5.1, "altitude": 670.0}
    ]
}

# Ruta 2: Sendero Barcelona - Parque Güell
route2 = {
    "device_id": "device_bcn_002", 
    "points": [
        {"lat": 41.4144, "lon": 2.1527, "timestamp": "2024-01-16T10:00:00Z", "accuracy": 3.5, "altitude": 150.0},
        {"lat": 41.4148, "lon": 2.1530, "timestamp": "2024-01-16T10:05:00Z", "accuracy": 4.0, "altitude": 155.0},
        {"lat": 41.4152, "lon": 2.1535, "timestamp": "2024-01-16T10:10:00Z", "accuracy": 3.2, "altitude": 160.0},
        {"lat": 41.4156, "lon": 2.1540, "timestamp": "2024-01-16T10:15:00Z", "accuracy": 4.5, "altitude": 165.0},
        {"lat": 41.4160, "lon": 2.1545, "timestamp": "2024-01-16T10:20:00Z", "accuracy": 3.8, "altitude": 170.0}
    ]
}

# Ruta 3: Sendero Sevilla - Parque de María Luisa
route3 = {
    "device_id": "device_sev_003",
    "points": [
        {"lat": 37.3754, "lon": -5.9866, "timestamp": "2024-01-17T08:30:00Z", "accuracy": 4.8, "altitude": 25.0},
        {"lat": 37.3758, "lon": -5.9870, "timestamp": "2024-01-17T08:35:00Z", "accuracy": 3.9, "altitude": 28.0},
        {"lat": 37.3762, "lon": -5.9875, "timestamp": "2024-01-17T08:40:00Z", "accuracy": 4.2, "altitude": 30.0},
        {"lat": 37.3766, "lon": -5.9880, "timestamp": "2024-01-17T08:45:00Z", "accuracy": 5.0, "altitude": 32.0},
        {"lat": 37.3770, "lon": -5.9885, "timestamp": "2024-01-17T08:50:00Z", "accuracy": 3.7, "altitude": 35.0}
    ]
}

def create_routes():
    routes = [route1, route2, route3]
    created_routes = []
    
    for i, route in enumerate(routes, 1):
        try:
            response = requests.post(f"{BASE_URL}/routes", json=route)
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Ruta {i} creada: {result}")
                created_routes.append(result)
            else:
                print(f"❌ Error creando ruta {i}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"❌ Error de conexión ruta {i}: {e}")
    
    return created_routes

if __name__ == "__main__":
    print("🚀 Creando rutas de ejemplo...")
    created_routes = create_routes()
    print(f"\n✅ Se crearon {len(created_routes)} rutas exitosamente")