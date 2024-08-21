import uuid
from datetime import datetime

from api.v1.models.base_model import BaseTableModel
from sqlalchemy import (
    ARRAY,
    UUID,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship


class Company(BaseTableModel):
    __tablename__ = "companies"

    id = Column(String(255), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    website = Column(String(255))
    industry = Column(String(255))
    headquarters = Column(String(255))
    culture_summary = Column(Text)  # AI-generated summary of company culture
    hiring_patterns = Column(Text)  # AI-generated insights on hiring patterns
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    recruiters = relationship("Recruiter", back_populates="company")
