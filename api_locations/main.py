from fastapi import FastAPI
from app.routers import location, routes


fastapi_app = FastAPI(title="Senderos GPS API")

# Incluye todos los routers que necesites
for r in (location.router, routes.router):
    fastapi_app.include_router(r)

@fastapi_app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:fastapi_app", host="0.0.0.0", port=port)

