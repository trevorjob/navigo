# app/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    ARRAY,
    ForeignKey,
)
from api.v1.models.base_model import BaseTableModel
from datetime import datetime
from sqlalchemy.orm import relationship


class Education(BaseTableModel):
    __tablename__ = "educations"

    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    institution_name = Column(String(255))
    degree = Column(String(255))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    description = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="educations")
