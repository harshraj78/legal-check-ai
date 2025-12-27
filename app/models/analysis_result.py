import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.models.base import Base


class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    contract_id = Column(
        UUID(as_uuid=True),
        ForeignKey("contracts.id", ondelete="CASCADE"),
        nullable=False,
    )

    risk_level = Column(String(50), nullable=False)
    clause_flag = Column(String(255), nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    contract = relationship(
        "Contract",
        back_populates="analysis_results",
    )
