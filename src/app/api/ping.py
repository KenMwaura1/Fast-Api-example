from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db import get_db

router = APIRouter()


class PingResponse(BaseModel):
    """Ping response schema"""

    status: str
    message: str


@router.get(
    "/ping",
    response_model=PingResponse,
    tags=["health"],
    summary="Health check endpoint",
)
async def pong(session: AsyncSession = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity.

    Returns the current status of the API and database connection.
    """
    try:
        # Verify database connection by executing a simple query
        await session.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"

    if db_status == "disconnected":
        return PingResponse(
            status="degraded",
            message="API is running but database connection is unavailable",
        )

    return PingResponse(status="healthy", message="API and database are operational")
