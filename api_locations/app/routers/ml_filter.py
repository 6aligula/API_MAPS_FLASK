from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from uuid import uuid4
from pydantic import BaseModel
from typing import List
from ..schemas.route import RouteDetail, RoutePoint
from ..utils.ml_filter_route import filter_route_points_ml
from ..core.firestore import get_db
from ..services.location_service import LocationService

router = APIRouter(prefix="/ml-filter", tags=["ML-Filter"])

class MLFilterRequest(BaseModel):
    device_id: str
    start_date: str
    end_date: str

@router.post("", response_model=RouteDetail)
def ml_filter_route(payload: MLFilterRequest):
    """
    Endpoint que filtra puntos usando los datos de la colección Location para un device_id dado,
    eliminando outliers (con DBSCAN) según un rango de fechas, y retorna un objeto RouteDetail.
    """
    try:
        start_date_obj = datetime.fromisoformat(payload.start_date)
        end_date_obj   = datetime.fromisoformat(payload.end_date)
        # Si las fechas son naive, asumir UTC
        if start_date_obj.tzinfo is None:
            start_date_obj = start_date_obj.replace(tzinfo=timezone.utc)
        if end_date_obj.tzinfo is None:
            end_date_obj = end_date_obj.replace(tzinfo=timezone.utc)
    except Exception:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido. Se espera ISO.")

    db = get_db()
    loc_service = LocationService(db)
    
    # Buscar el documento de ubicaciones para el dispositivo
    doc = loc_service._find_device_document(payload.device_id)
    if not doc:
        raise HTTPException(status_code=404, detail="No se encontraron datos de ubicación para este dispositivo")

    # Recuperar la lista de entradas ubicacionales (LocationEntry)
    raw_points = loc_service.get_location_entries_by_doc(doc.id)
    if not raw_points:
        raise HTTPException(status_code=404, detail="No se encontraron entradas en la colección Location.")

    # Convertir cada LocationEntry a RoutePoint
    route_points: List[RoutePoint] = []
    for location_entry in raw_points:
        route_point = RoutePoint(
            lat=location_entry.lat,
            lon=location_entry.lon,
            timestamp=location_entry.timestamp,
            accuracy=location_entry.accuracy,
            altitude=location_entry.altitude,
            speed=location_entry.speed
        )
        route_points.append(route_point)

    # Filtrar puntos usando el algoritmo ML (DBSCAN)
    filtered_points = filter_route_points_ml(route_points, start_date_obj, end_date_obj)
    if not filtered_points:
        raise HTTPException(status_code=400, detail="No se obtuvieron puntos válidos tras la limpieza.")

    return RouteDetail(
        id=str(uuid4()),
        device_id=payload.device_id,
        created_at=datetime.utcnow(),
        last_update=datetime.utcnow(),
        points=filtered_points
    )