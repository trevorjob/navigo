# app/models.py

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Text,
    DateTime,
    JSON,
    ForeignKey,
)
from api.v1.models.base_model import BaseTableModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList


class Project(BaseTableModel):
    __tablename__ = "projects"

    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE"))
    project_name = Column(String(255))
    description = Column(Text)
    technologies = Column(MutableList.as_mutable(JSON), default=[])
    project_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="projects")
