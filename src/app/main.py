from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import notes, ping, auth
from app.db import engine
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    yield
    print("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title="Notes API",
    description="A simple API for managing notes with search and filtering",
    version="1.0.0",
    lifespan=lifespan,
)


settings = get_settings()

# CORS configuration - only allow specific origins in production
allowed_origins = settings.allowed_origins.split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(notes.router, prefix="/notes", tags=["notes"])
