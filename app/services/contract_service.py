from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from pathlib import Path
import shutil
import logging
import fitz  # PyMuPDF

from app.core.config import settings
from app.models.contract import Contract, AnalysisResult
from app.integrations.llm_service import LLMService


logger = logging.getLogger(__name__)


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
        db.refresh(contract)

        file_path = settings.STORAGE_DIR / f"{contract.id}.pdf"

        try:
            # 3. Save PDF to disk
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

            # 4. Extract text from PDF
            extracted_text = ContractService.extract_text_from_pdf(file_path)

            # 5. Store extracted text
            contract.raw_text = extracted_text
            db.commit()

            # 6. AI Analysis
            logger.info(f"Starting AI analysis for contract {contract.id}")

            llm = LLMService()
            analysis = llm.analyze_contract_text(extracted_text)

            analysis_result = AnalysisResult(
                contract_id=contract.id,
                risk_score=analysis["risk_score"],
                summary=analysis["summary"]
            )

            db.add(analysis_result)
            contract.status = "completed"
            db.commit()

            logger.info(f"AI analysis completed for contract {contract.id}")

        except Exception as e:
            logger.exception(f"Contract processing failed: {contract.id}")
            contract.status = "failed"
            db.commit()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to process contract"
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
