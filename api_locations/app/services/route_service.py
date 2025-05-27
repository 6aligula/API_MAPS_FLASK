from uuid import uuid4
from datetime import datetime
from google.cloud.firestore import Client, ArrayUnion
from ..schemas.route import RouteDetail, RoutePoint, RouteSummary
from ..core.config import get_settings

class RouteService:
    def __init__(self, db: Client):
        settings = get_settings()
        self.col = db.collection(settings.collection_name_routes)

    # ---------- escritura opcional ----------
    def create_route(self, device_id: str, points: list[RoutePoint]) -> str:
        """Crea una nueva ruta y devuelve su uuid."""
        route_id = str(uuid4())
        now = datetime.utcnow()

        # Serializar puntos a dict
        _points = [p.model_dump() for p in points]

        self.col.document(route_id).set({
            "device_id": device_id,
            "created_at": now,
            "last_update": now,
            "points": _points
        })
        return route_id

    # ---------- lectura ----------
    def list_routes(self) -> list[RouteSummary]:
        """Devuelve un resumen de todas las rutas (paginable si quieres)."""
        snaps = self.col.stream()
        return [
            RouteSummary(
                id=snap.id,
                device_id=data.get("device_id", "unknown"),
                created_at=data.get("created_at"),
                last_update=data.get("last_update")
            )
            for snap in snaps
            if (data := snap.to_dict())
        ]

    def get_route(self, route_id: str) -> RouteDetail:
        doc = self.col.document(route_id).get()
        if not doc.exists:
            raise ValueError(f"Ruta con ID {route_id} no encontrada")

        data = doc.to_dict()
        
        # Convertir los puntos de dict a RoutePoint
        points = [
            RoutePoint(**point_data) 
            for point_data in data.get("points", [])
        ]
        
        return RouteDetail(
            id=route_id,
            device_id=data.get("device_id", "unknown"),
            created_at=data.get("created_at"),
            last_update=data.get("last_update"),
            points=points
        )