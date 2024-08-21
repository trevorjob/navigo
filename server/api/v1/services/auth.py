from api.core.base.services import Service
from api.db.database import get_db
from api.v1.models.user import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends, Request
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from api.v1.schemas.auth import *
from api.v1.schemas.user import UserCreate, UserUpdate
import datetime as dt
from datetime import datetime, timedelta
from api.utils.db_validators import check_model_existence
from api.utils.settings import settings
from api.utils.tokens import is_token_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def create(self, db: Session, schema: UserCreate):
        """Creates a new user"""

        if db.query(User).filter(User.email == schema.email).first():
            raise HTTPException(
                status_code=400,
                detail="User with this email already exists",
            )

        # Hash password
        schema.password = self.hash_password(password=schema.password)

        # Create user object with hashed password and other attributes from schema
        user = User(**schema.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)

        db.commit()

        return user

    def delete(self, db: Session, id=None, access_token: str = Depends(oauth2_scheme)):
        """Function to soft delete a user"""

        # Get user from access token if provided, otherwise fetch user by id
        user = (
            self.get_current_user(access_token, db)
            if id is None
            else check_model_existence(db, User, id)
        )

        user.is_deleted = True
        db.commit()

        return super().delete()

    def perform_user_check(self, user: User):
        """This checks if a user is active and verified and not a deleted user"""

        if not user.is_active:
            raise HTTPException(detail="User is not active", status_code=403)

    def hash_password(self, password: str) -> str:
        """Function to hash a password"""

        hashed_password = pwd_context.hash(secret=password)
        return hashed_password

    def verify_password(self, password: str, hash: str) -> bool:
        """Function to verify a hashed password"""

        return pwd_context.verify(secret=password, hash=hash)

    def create_access_token(self, user_id: str) -> str:
        """Function to create access token"""

        expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        data = {"user_id": user_id, "exp": expires, "type": "access"}
        encoded_jwt = jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    def create_refresh_token(self, user_id: str) -> str:
        """Function to create access token"""

        expires = dt.datetime.now(dt.timezone.utc) + dt.timedelta(
            days=settings.JWT_REFRESH_EXPIRY
        )
        data = {"user_id": user_id, "exp": expires, "type": "refresh"}
        encoded_jwt = jwt.encode(data, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt

    def verify_access_token(self, access_token: str, credentials_exception):
        """Funtcion to decode and verify access token"""

        try:
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("user_id")
            token_type = payload.get("type")

            if user_id is None:
                raise credentials_exception

            if token_type == "refresh":
                raise HTTPException(detail="Refresh token not allowed", status_code=400)

            token_data = TokenData(id=user_id)

        except JWTError as err:
            print(err)
            raise credentials_exception

        return token_data

    def verify_refresh_token(self, refresh_token: str, credentials_exception):
        """Funtcion to decode and verify refresh token"""

        try:
            payload = jwt.decode(
                refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            user_id = payload.get("user_id")
            token_type = payload.get("type")

            if user_id is None:
                raise credentials_exception

            if token_type == "access":
                raise HTTPException(detail="Access token not allowed", status_code=400)

            token_data = TokenData(id=user_id)

        except JWTError:
            raise credentials_exception

        return token_data

    def refresh_access_token(self, current_refresh_token: str):
        """Function to generate new access token and rotate refresh token"""

        credentials_exception = HTTPException(
            status_code=401, detail="Refresh token expired"
        )

        token = self.verify_refresh_token(current_refresh_token, credentials_exception)

        if token:
            access = self.create_access_token(user_id=token.id)
            refresh = self.create_refresh_token(user_id=token.id)

            return access, refresh

    def get_current_user(
        self, access_token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ) -> User:
        """Function to get current logged in user"""
        if is_token_blacklisted(access_token, db):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
            )

        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token = self.verify_access_token(access_token, credentials_exception)
        user = db.query(User).filter(User.id == token.id).first()

        return user

    def authenticate_user(self, db: Session, email: str, password: str):
        """Function to authenticate a user"""

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=400, detail="Invalid user credentials")

        if not self.verify_password(password, user.password):
            raise HTTPException(status_code=400, detail="Invalid user credentials")

        return user

    def change_password(
        self,
        old_password: str,
        new_password: str,
        user: User,
        db: Session,
    ):
        """Endpoint to change the user's password"""

        if not self.verify_password(old_password, user.password):
            raise HTTPException(status_code=400, detail="Incorrect old password")

        user.password = self.hash_password(new_password)
        db.commit()


auth_service = AuthService()
