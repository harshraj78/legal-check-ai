from fastapi import APIRouter
from app.api.v1.endpoints import contracts

api_router = APIRouter()

api_router.include_router(
    contracts.router,
    prefix="/contracts",
    tags=["contracts"],
)
