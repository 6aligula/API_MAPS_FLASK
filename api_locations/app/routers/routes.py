from fastapi import APIRouter, HTTPException, status
from typing import List
from ..core.firestore import get_db
from ..services.route_service import RouteService
from ..schemas.route import RouteSummary, RouteDetail

router = APIRouter(prefix="/routes", tags=["Routes"])

@router.get("", response_model=List[RouteSummary])
def get_list_routes():
    db = get_db()
    service = RouteService(db)
    return service.list_routes()

@router.get("/{route_id}", response_model=RouteDetail)
def get_route(route_id: str):
    db = get_db()
    service = RouteService(db)
    try:
        return service.get_route(route_id)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )