import shutil
import logging
from pathlib import Path
from uuid import UUID

import fitz
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.contract import Contract, AnalysisResult
from app.integrations.llm_service import LLMService

logger = logging.getLogger(__name__)


class ContractService:
    # ---------- FAST ----------
    @staticmethod
    async def create_contract_record(db: Session, file: UploadFile) -> Contract:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed",
            )

        settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)

        contract = Contract(
            filename=file.filename,
            status="pending",
        )

        db.add(contract)
        db.commit()
        db.refresh(contract)

        file_path = settings.STORAGE_DIR / f"{contract.id}.pdf"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return contract

    # ---------- SLOW ----------
    @staticmethod
    def process_contract_analysis(contract_id: UUID):
        from app.core.db import SessionLocal

        db = SessionLocal()
        try:
            contract = db.query(Contract).filter_by(id=contract_id).first()
            if not contract:
                return

            logger.info(f"Processing contract {contract_id}")

            # 1. Extract text
            text = ContractService.extract_text_from_pdf(
                settings.STORAGE_DIR / f"{contract_id}.pdf"
            )
            contract.raw_text = text
            db.commit()

            # 2. AI Analysis
            llm = LLMService()
            analysis = llm.analyze_contract_text(text)

            # 3. Save result
            result = AnalysisResult(
                contract_id=contract_id,
                risk_score=analysis["risk_score"],
                summary=analysis["summary"],
            )
            db.add(result)

            contract.status = "completed"
            db.commit()

            logger.info(f"Completed contract {contract_id}")

        except Exception as e:
            logger.exception(f"Failed contract {contract_id}")
            if contract:
                contract.status = "failed"
                db.commit()
        finally:
            db.close()

    @staticmethod
    def get_contract_with_analysis(db: Session, contract_id: UUID):
        contract = (
            db.query(Contract)
            .filter(Contract.id == contract_id)
            .first()
        )

        if not contract:
            raise HTTPException(status_code=404, detail="Contract not found")

        return {
            "id": contract.id,
            "filename": contract.filename,
            "status": contract.status,
            "risk_score": contract.analysis.risk_score if contract.analysis else None,
            "summary": contract.analysis.summary if contract.analysis else None,
        }

    @staticmethod
    def extract_text_from_pdf(file_path: Path) -> str:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()
