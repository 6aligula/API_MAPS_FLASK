from functools import lru_cache
from pydantic import Field, AliasChoices
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # ID del proyecto
    project_id: str = Field(
        ...,
        validation_alias=AliasChoices("GCP_PROJECT", "GOOGLE_CLOUD_PROJECT")
    )

    # colección para los documentos de localizaciones
    collection_name: str = Field(
        default="locations",
        validation_alias=AliasChoices("LOCATIONS_COLLECTION",
                                      "COLLECTION_LOCATIONS")
    )

    #  NUEVA colección para las rutas
    collection_name_routes: str = Field(
        default="rutas",
        validation_alias=AliasChoices("ROUTES_COLLECTION",
                                      "COLLECTION_ROUTES")
    )

    # Config del modelo
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="",
        populate_by_name=True
    )

@lru_cache
def get_settings() -> Settings:
    import os
    print("ENV DEBUG:", {k: v for k, v in os.environ.items() if "PROJECT" in k})
    return Settings()
