from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.services.contract_service import ContractService

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_contract(
    file: UploadFile = File(..., description="The PDF contract to analyze"),
    db: Session = Depends(get_db)
):
    contract = await ContractService.create_contract(db, file)

    return {
        "id": contract.id,
        "filename": contract.filename,
        "status": contract.status
    }


@router.get("/{contract_id}")
def get_contract_status(
    contract_id: UUID,
    db: Session = Depends(get_db)
):
    contract = ContractService.get_contract(db, contract_id)

    return {
        "id": contract.id,
        "filename": contract.filename,
        "status": contract.status
    }
