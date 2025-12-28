from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.init_db import init_db

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

# Versioned routes
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
def health_check():
    # TODO: In next sprint, add DB connectivity check here
    return {"status": "healthy"}

@app.on_event("startup")
def on_startup():
    init_db()