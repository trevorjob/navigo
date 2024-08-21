from pydantic import BaseModel, EmailStr
from typing import Optional


class LoginReq(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema to structure token data"""

    id: Optional[str]
