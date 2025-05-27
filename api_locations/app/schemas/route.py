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

class RouteSummary(BaseModel):
    id: str                           # UUID de la ruta
    device_id: str                    # Quién la generó (opcional pero útil)
    created_at: datetime
    last_update: datetime

class RouteDetail(RouteSummary):
    points: List[RoutePoint] = Field(default_factory=list)
