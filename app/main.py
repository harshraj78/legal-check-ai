from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import router as api_v1_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

# Versioned API mount
app.include_router(api_v1_router, prefix=settings.API_V1_STR)
