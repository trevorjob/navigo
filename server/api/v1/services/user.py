from typing import Any, Optional

from api.core.base.services import Service
from api.db.database import get_db
from api.utils.db_validators import check_model_existence
from api.utils.settings import settings
from api.v1.models.user import User
from api.v1.schemas.user import UserUpdate
from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session


class UserService:
    """User service"""

    def fetch_all(
        self, db: Session, page: int, per_page: int, **query_params: Optional[Any]
    ):
        """
        Fetch all users
        Args:
            db: database Session object
            page: page number
            per_page: max number of users in a page
            query_params: params to filter by
        """
        per_page = min(per_page, 10)

        # Enable filter by query parameter
        filters = []
        if all(query_params):
            # Validate boolean query parameters
            for param, value in query_params.items():
                if value is not None and not isinstance(value, bool):
                    raise HTTPException(
                        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        detail=f"Invalid value for '{param}'. Must be a boolean.",
                    )
                if value == None:
                    continue
                if hasattr(User, param):
                    filters.append(getattr(User, param) == value)
        query = db.query(User)
        total_users = query.count()
        if filters:
            query = query.filter(*filters)
            total_users = query.count()

        all_users: list = (
            query.order_by(desc(User.created_at))
            .limit(per_page)
            .offset((page - 1) * per_page)
            .all()
        )

        return self.all_users_response(all_users, total_users, page, per_page)

    def fetch(self, db: Session, id):
        """Fetches a user by their id"""

        user = check_model_existence(db, User, id)

        # return user if user is not deleted
        return user

    def get_user_by_id(self, db: Session, id: str):
        """Fetches a user by their id"""

        user = check_model_existence(db, User, id)
        return user

    def fetch_by_email(self, db: Session, email):
        """Fetches a user by their email"""

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    def update(self, db: Session, current_user: User, schema: UserUpdate, id=None):
        """Function to update a User"""

        # Get user from access token if provided, otherwise fetch user by id
        if db.query(User).filter(User.email == schema.email).first():
            raise HTTPException(
                status_code=400,
                detail="User with this email or username already exists",
            )

        user = self.fetch(db=db, id=id)

        update_data = schema.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user


user_service = UserService()
