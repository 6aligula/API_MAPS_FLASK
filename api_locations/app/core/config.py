from functools import lru_cache
from pydantic import Field, AliasChoices          # AliasChoices para varios nombres
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Acepta GCP_PROJECT **y** GOOGLE_CLOUD_PROJECT
    project_id: str = Field(
        ...,
        validation_alias=AliasChoices("GCP_PROJECT", "GOOGLE_CLOUD_PROJECT")  # ⬅️
    )
    collection_name: str = "locations"

    # Configuración del modelo
    model_config = SettingsConfigDict(
        env_file=".env",         # como ya tenías
        env_prefix="",           # sin prefijo; usamos alias explícitos
        populate_by_name=True    # permite usar project_id en tests/local
    )

@lru_cache
def get_settings() -> Settings:
    import os
    # Se queda tu debug para Cloud Logging
    print("🧪 ENV DEBUG:", {k: v for k, v in os.environ.items() if "PROJECT" in k})
    return Settings()
