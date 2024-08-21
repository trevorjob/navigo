# app/models.py

from datetime import datetime

from api.v1.models.base_model import BaseTableModel
from sqlalchemy import (
    ARRAY,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship


class WorkExperience(BaseTableModel):
    __tablename__ = "work_experiences"

    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    company_name = Column(String(255))
    role = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="work_experiences")
