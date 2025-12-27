from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.contract import Contract


class ContractService:
    @staticmethod
    async def create_contract(db: Session, file: UploadFile) -> Contract:
        # 1. Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only PDFs are allowed."
            )

        # 2. Create DB record
        contract = Contract(
            filename=file.filename,
            status="pending"
        )

        db.add(contract)
        db.commit()
        db.refresh(contract)  # IMPORTANT

        return contract

    @staticmethod
    def get_contract(db: Session, contract_id: UUID) -> Contract:
        contract = db.query(Contract).filter(Contract.id == contract_id).first()

        if not contract:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Contract not found"
            )

        return contract
