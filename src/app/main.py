from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.api import notes, ping
from app.db import engine, metadata, database


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    metadata.create_all(engine)
    await database.connect()
    yield
    print("Shutting down...")
    await database.disconnect()

app = FastAPI(
    title="Notes API",
    description="A simple API for managing notes with search and filtering",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration - only allow specific origins in production
allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost,http://localhost:8080,http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(notes.router, prefix="/notes", tags=["notes"])
