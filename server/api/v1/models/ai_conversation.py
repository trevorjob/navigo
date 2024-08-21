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


class Conversation(BaseTableModel):
    __tablename__ = "conversations"

    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    message = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="conversations")
