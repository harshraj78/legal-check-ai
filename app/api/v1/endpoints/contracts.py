from fastapi import APIRouter

router = APIRouter()

@router.post("/upload")
async def upload_contract():
    return {"message": "Endpoint ready for contract analysis"}