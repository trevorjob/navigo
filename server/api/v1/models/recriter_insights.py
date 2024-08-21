from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
    Text,
    ARRAY,
    UUID,
    Float,
)
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid


from api.v1.models.base_model import BaseTableModel


class Recruiter(BaseTableModel):
    __tablename__ = "recruiters"

    name = Column(String(255), nullable=False)
    company_id = Column(String(255), ForeignKey("companies.id"))
    linkedin_url = Column(String(255))
    email = Column(String(255))
    insights = Column(Text)  # Insights gathered through AI analysis
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="recruiters")
