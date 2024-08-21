from typing import Annotated, Optional, Literal
from fastapi import Depends, APIRouter, Request, status, Query, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from api.utils.responses import success_response
from api.v1.models.user import User
from api.v1.schemas.user import (
    # DeactivateUserSchema,
    ChangePasswordSchema,
    # ChangePwdRet,
    # AllUsersResponse,
    UserUpdate,
    # AdminCreateUserResponse,
    # AdminCreateUser,
)
from api.db.database import get_db
from api.v1.services.user import user_service
from api.v1.services.auth import auth_service


user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.get("/me", status_code=status.HTTP_200_OK, response_model=success_response)
def get_current_user_details(
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Endpoint to get current user details"""

    return success_response(
        status_code=200,
        message="User details retrieved successfully",
        data=jsonable_encoder(
            current_user,
            exclude=[
                "password",
                "updated_at",
            ],
        ),
    )


@user_router.get("/delete", status_code=200)
async def delete_account(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Endpoint to delete a user account"""

    # Delete current user
    auth_service.delete(db=db, id=current_user.id)

    return success_response(
        status_code=200,
        message="User deleted successfully",
    )


@user_router.patch("/me/password", status_code=200)
async def change_password(
    schema: ChangePasswordSchema,
    db: Session = Depends(get_db),
    user: User = Depends(auth_service.get_current_user),
):
    """Endpoint to change the user's password"""

    auth_service.change_password(schema.old_password, schema.new_password, user, db)

    return success_response(status_code=200, message="Password changed successfully")


@user_router.patch("/me", status_code=status.HTTP_200_OK)
def update_current_user(
    current_user: Annotated[User, Depends(auth_service.get_current_user)],
    schema: UserUpdate,
    db: Session = Depends(get_db),
):

    user = user_service.update(db=db, schema=schema, current_user=current_user)

    return success_response(
        status_code=status.HTTP_200_OK,
        message="User Updated Successfully",
        data=jsonable_encoder(
            user,
            exclude=[
                "password",
                "updated_at",
                "created_at",
            ],
        ),
    )
