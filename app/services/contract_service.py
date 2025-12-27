from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pathlib import Path
import shutil
import fitz  # PyMuPDF


from app.core import db
from app.core.config import settings

from app.models.contract import Contract


class ContractService:
    @staticmethod
    async def create_contract(db: Session, file: UploadFile) -> Contract:
        # Ensure storage directory exists
        settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        # 1. Validate file type
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file type. Only PDFs are allowed."
            )

        # 2. Create DB record
        contract = Contract(
            filename=file.filename,
            status="processing"
        )

        db.add(contract)
        db.commit()
        db.refresh(contract)  # IMPORTANT
        
        file_path = settings.STORAGE_DIR / f"{contract.id}.pdf"

        try:
            # Save PDF to disk
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # Extract text from PDF
            extracted_text = ContractService.extract_text_from_pdf(file_path)

            # Update DB with extracted content
            contract.raw_text = extracted_text
            contract.status = "completed"
            db.commit()

        except Exception:
            contract.status = "failed"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process PDF"
            )

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
    
    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        text = ""

        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()

        return text.strip()

