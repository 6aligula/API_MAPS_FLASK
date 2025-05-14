from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class LocationEntry(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    timestamp: datetime
    accuracy: Optional[float] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None

class LocationIn(BaseModel):
    device_id: str = Field(..., min_length=1)
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)
    timestamp: datetime | None = None  # opcional; servidor pondrá ahora()
    accuracy: Optional[float] = None
    altitude: Optional[float] = None
    speed: Optional[float] = None

class LocationOut(BaseModel):
    id: str
    device_id: str
    created_at: datetime
    last_update: datetime
    locations: List[LocationEntry]