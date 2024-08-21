from contextlib import asynccontextmanager

import uvicorn
from api.db.database import create_database
from api.v1.routes import api_v1
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function"""
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Navigo AI Assistant",
    description="fully integrated job coach",
    version="1.0.0",
)
origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

# app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_v1)
create_database()


@app.get("/", tags=["Home"])
async def get_root(request: Request) -> dict:
    return {
        "message": "Welcome to API",
        "status_code": status.HTTP_200_OK,
        "data": {"URL": ""},
    }


if __name__ == "__main__":
    uvicorn.run("main:app", port=7001, reload=True)
