from pydantic import BaseModel, Field
from datetime import datetime

class LocationIn(BaseModel):
    device_id: str  = Field(..., min_length=1)
    lat:       float = Field(..., ge=-90,  le=90)
    lon:       float = Field(..., ge=-180, le=180)
    timestamp: datetime | None = None     # opcional; servidor pondrá ahora()

class LocationOut(LocationIn):
    id: str
