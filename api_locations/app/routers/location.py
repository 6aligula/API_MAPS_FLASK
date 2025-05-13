from fastapi import APIRouter, status
from ..core.firestore import get_db
from ..schemas.location import LocationIn, LocationOut
from ..services.location_service import LocationService

router = APIRouter(prefix="/location", tags=["Location"])

@router.post("", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def post_location(payload: LocationIn):
    print("📥 Payload recibido:", payload.model_dump())
    db = get_db()
    service = LocationService(db)
    doc_id = service.save(payload)
    print("✅ Documento guardado con ID:", doc_id)
    return LocationOut(id=doc_id, **payload.model_dump())

