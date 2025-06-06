from fastapi import APIRouter, status, HTTPException
from ..core.firestore import get_db
from ..schemas.location import LocationIn, LocationOut
from ..services.location_service import LocationService

router = APIRouter(prefix="/location", tags=["Location"])

@router.post("", response_model=LocationOut, status_code=status.HTTP_201_CREATED)
def post_location(payload: LocationIn):
    print("Payload recibido:", payload.model_dump())
    db = get_db()
    service = LocationService(db)
    
    try:
        result = service.save(payload)
        print(" Documento guardado con ID:", result)
        return result
    except Exception as e:
        print(f" Error al guardar la ubicación: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error guardando la ubicación: {str(e)}"
        )

