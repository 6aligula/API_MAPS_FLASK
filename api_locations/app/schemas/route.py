from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

class RoutePoint(BaseModel):
    lat: float
    lon: float
    timestamp: datetime
    accuracy: Optional[float] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None

# Nuevo esquema para la entrada de ruta
class RouteIn(BaseModel):
    device_id: str = Field(..., min_length=1)
    points: List[RoutePoint] = Field(..., min_items=2, description="Mínimo 2 puntos para una ruta")

class RouteCreateResponse(BaseModel):
    route_id: str
    message: str
class RouteSummary(BaseModel):
    id: str                           # UUID de la ruta
    device_id: str                    # Quién la generó (opcional pero útil)
    created_at: datetime
    last_update: datetime

class RouteDetail(RouteSummary):
    points: List[RoutePoint] = Field(default_factory=list)
