from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    status,
    BackgroundTasks,
)
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.services.contract_service import ContractService

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_202_ACCEPTED)
async def upload_contract(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # 1. Fast operation (DB + file only)
    contract = await ContractService.create_contract_record(db, file)

    # 2. Slow operation (background)
    background_tasks.add_task(
        ContractService.process_contract_analysis,
        contract.id,
    )

    return {
        "id": contract.id,
        "status": contract.status,
        "message": "Analysis started in background",
    }


@router.get("/{contract_id}")
def get_contract_details(
    contract_id: UUID,
    db: Session = Depends(get_db),
):
    return ContractService.get_contract_with_analysis(db, contract_id)
