from fastapi import FastAPI
from app.routers import location

fastapi_app = FastAPI(title="Senderos GPS API")
fastapi_app.include_router(location.router)

@fastapi_app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    import os

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app.main:fastapi_app", host="0.0.0.0", port=port)

