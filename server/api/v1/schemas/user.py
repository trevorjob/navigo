from pydantic import BaseModel, EmailStr
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    profile_picture_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    skills: Optional[list[str]] = None
    portfolio_links: Optional[list[str]] = None
    resume_url: Optional[str] = None

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str