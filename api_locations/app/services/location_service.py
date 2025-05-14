from uuid import uuid4
from datetime import datetime
from google.cloud.firestore import Client
from google.cloud import firestore
from ..schemas.location import LocationIn, LocationEntry, LocationOut
from ..core.config import get_settings

class LocationService:
    def __init__(self, db: Client):
        settings = get_settings()
        self.col = db.collection(settings.collection_name)

    def save(self, data: LocationIn) -> LocationOut:
        """Método principal que orquesta el guardado de localizaciones."""
        payload = data.model_dump()
        timestamp = payload["timestamp"] or datetime.utcnow()
        
        # Buscar si ya existe un documento para este dispositivo
        doc = self._find_device_document(data.device_id)
        location_entry = self._create_location_entry(data, timestamp)
        
        if doc:
            # Actualizar documento existente
            doc_id = self._update_existing_document(doc, location_entry, timestamp)
            return self._get_location_by_id(doc_id)
        else:
            # Crear nuevo documento
            doc_id = self._create_new_document(data.device_id, location_entry, timestamp)
            return self._get_location_by_id(doc_id)
    
    def _find_device_document(self, device_id: str):
        """Busca un documento existente para el dispositivo dado."""
        query = self.col.where("device_id", "==", device_id).limit(1).stream()
        docs = list(query)
        return docs[0] if docs else None
    
    def _create_location_entry(self, data: LocationIn, timestamp: datetime) -> dict:
        """Crea un objeto LocationEntry a partir de los datos de entrada."""
        return {
            "lat": data.lat,
            "lon": data.lon,
            "timestamp": timestamp,
            "accuracy": data.accuracy,
            "altitude": data.altitude,
            "speed": data.speed
        }
    
    def _update_existing_document(self, doc, location_entry: dict, timestamp: datetime) -> str:
        """Actualiza un documento existente con una nueva localización."""
        doc_ref = self.col.document(doc.id)
        doc_ref.update({
            "locations": firestore.ArrayUnion([location_entry]),
            "last_update": timestamp
        })
        return doc.id
    
    def _create_new_document(self, device_id: str, location_entry: dict, timestamp: datetime) -> str:
        """Crea un nuevo documento para un dispositivo."""
        doc_id = str(uuid4())
        self.col.document(doc_id).set({
            "device_id": device_id,
            "created_at": timestamp,
            "last_update": timestamp,
            "locations": [location_entry]
        })
        return doc_id
        
    
    def _get_location_by_id(self, doc_id: str) -> LocationOut:
        """Recupera un documento de ubicación por su ID y lo convierte al modelo LocationOut."""
        print(f"🔍 Buscando documento con ID: {doc_id}")
        doc_ref = self.col.document(doc_id).get()
        if not doc_ref.exists:
            raise ValueError(f"Documento con ID {doc_id} no encontrado")
            
        data = doc_ref.to_dict()
        print(f"Datos recuperados: {data}")
        current_time = datetime.utcnow()
        
        # Obtener valores con defaults seguros
        device_id = data.get("device_id", "unknown")
        created_at = data.get("created_at", current_time)
        last_update = data.get("last_update", current_time)
        locations_raw = data.get("locations", [])
        
        # Asegurarse que locations sea una lista
        if not isinstance(locations_raw, list):
            locations_raw = [locations_raw] if locations_raw else []
        
        # Procesar cada ubicación
        processed_locations = []
        for loc in locations_raw:
            loc_copy = {
                "lat": loc.get("lat", 0.0),
                "lon": loc.get("lon", 0.0),
                "timestamp": loc.get("timestamp", current_time),
                "accuracy": loc.get("accuracy"),
                "altitude": loc.get("altitude"),
                "speed": loc.get("speed")
            }
            processed_locations.append(LocationEntry(**loc_copy))
        
        # Crear el objeto LocationOut directamente sin pasar por kwargs
        result = LocationOut(
            id=doc_id,
            device_id=device_id,
            created_at=created_at,
            last_update=last_update,
            locations=processed_locations
        )
        
        print(f"LocationOut creado: {result}")
        return result