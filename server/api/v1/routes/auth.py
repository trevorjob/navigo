from datetime import timedelta
from fastapi import BackgroundTasks, Depends, status, APIRouter, Response, Request
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.v1.models import User

# from api.v1.schemas.user import Token
from api.v1.schemas.user import UserCreate
from api.v1.schemas.auth import LoginReq
from api.db.database import get_db
from api.v1.services.user import user_service
from api.v1.services.auth import auth_service
from api.utils.responses import auth_response, success_response
from api.utils.tokens import blacklist_token

auth = APIRouter(prefix="/auth", tags=["Authentication"])


@auth.post(
    "/register", status_code=status.HTTP_201_CREATED, response_model=auth_response
)
def register(
    background_tasks: BackgroundTasks,
    response: Response,
    user_schema: UserCreate,
    db: Session = Depends(get_db),
):
    """Endpoint for a user to register their account"""

    # Create user account
    user = auth_service.create(db=db, schema=user_schema)

    # Create access and refresh tokens
    access_token = auth_service.create_access_token(user_id=user.id)
    refresh_token = auth_service.create_refresh_token(user_id=user.id)

    response = auth_response(
        status_code=201,
        message="User created successfully",
        access_token=access_token,
        data={"user": jsonable_encoder(user, exclude=["password", "updated_at"])},
    )

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=60),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response


@auth.post("/login", status_code=status.HTTP_200_OK, response_model=auth_response)
def login(login_request: LoginReq, db: Session = Depends(get_db)):
    """Endpoint to log in a user"""

    # Authenticate the user
    user = auth_service.authenticate_user(
        db=db, email=login_request.email, password=login_request.password
    )

    # Generate access and refresh tokens
    access_token = auth_service.create_access_token(user_id=user.id)
    refresh_token = auth_service.create_refresh_token(user_id=user.id)

    response = auth_response(
        status_code=200,
        message="Login successful",
        access_token=access_token,
        data={"user": jsonable_encoder(user, exclude=["password", "updated_at"])},
    )

    # Add refresh token to cookies
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        expires=timedelta(days=30),
        httponly=True,
        secure=True,
        samesite="none",
    )

    return response


@auth.post("/logout", status_code=status.HTTP_200_OK)
def logout(
    response: Response,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """Endpoint to log a user out of their account"""
    try:
        response = success_response(
            status_code=200, message="User logged put successfully"
        )

        token = request.headers.get("Authorization").replace("Bearer ", "")
        blacklist_token(token, db)

        # Delete refresh token from cookies
        response.delete_cookie(key="refresh_token")

        return response
    except Exception as e:
        raise e
