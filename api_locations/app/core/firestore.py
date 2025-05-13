from google.cloud import firestore
from .config import get_settings
from functools import lru_cache

@lru_cache
def get_db() -> firestore.Client:
    settings = get_settings()
    return firestore.Client(project=settings.project_id)
