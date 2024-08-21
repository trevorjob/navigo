# app/models.py

from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime, JSON
from api.v1.models.base_model import BaseTableModel
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList


class User(BaseTableModel):
    __tablename__ = "users"

    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    profile_picture_url = Column(Text)
    bio = Column(Text)
    location = Column(String(255))
    skills = Column(MutableList.as_mutable(JSON), default=[])
    portfolio_links = Column(MutableList.as_mutable(JSON), default=[])
    resume_url = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    work_experiences = relationship(
        "WorkExperience", back_populates="user", cascade="all, delete-orphan"
    )
    educations = relationship(
        "Education", back_populates="user", cascade="all, delete-orphan"
    )
    projects = relationship(
        "Project", back_populates="user", cascade="all, delete-orphan"
    )
    conversations = relationship(
        "Conversation", back_populates="user", cascade="all, delete-orphan"
    )
