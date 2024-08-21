""" The Profile model
"""

from sqlalchemy import Column, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from api.v1.models.base_model import BaseTableModel


class Profile(BaseTableModel):
    __tablename__ = "profiles"

    user_id = Column(
        String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )
    social = Column(Text, nullable=True)  # Assuming JSON or similar data type
    phone_number = Column(String, nullable=True)
    avatar_url = Column(String, nullable=True)
    recovery_email = Column(String, nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="profile")

    def to_dict(self):
        return {
            "id": self.id,
            "social": self.social,
            "bio": self.bio,
            "phone_number": self.phone_number,
            "avatar_url": self.avatar_url,
            "recovery_email": self.recovery_email,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "user": self.user.to_dict() if self.user else None,
        }
