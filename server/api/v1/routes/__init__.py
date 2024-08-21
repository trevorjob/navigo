from api.v1.routes.auth import auth
from api.v1.routes.user import user_router
from fastapi import APIRouter


api_v1 = APIRouter(prefix="/api/v1")

api_v1.include_router(auth)
api_v1.include_router(user_router)
