from uuid import uuid4
from datetime import datetime
from google.cloud.firestore import Client
from ..schemas.location import LocationIn
from ..core.config import get_settings

class LocationService:
    def __init__(self, db: Client):
        settings = get_settings()
        self.col = db.collection(settings.collection_name)

    def save(self, data: LocationIn) -> str:
        doc_id = str(uuid4())
        payload = data.model_dump()
        payload["timestamp"] = payload["timestamp"] or datetime.utcnow()
        self.col.document(doc_id).set(payload)
        return doc_id
