from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.db import database

router = APIRouter()


class PingResponse(BaseModel):
    """Ping response schema"""
    status: str
    message: str


@router.get(
    "/ping",
    response_model=PingResponse,
    tags=["health"],
    summary="Health check endpoint"
)
async def pong():
    """
    Health check endpoint to verify API and database connectivity.
    
    Returns the current status of the API and database connection.
    """
    try:
        # Verify database connection
        if not database.is_connected():
            return PingResponse(
                status="degraded",
                message="API is running but database connection is unavailable"
            )
        return PingResponse(
            status="healthy",
            message="API and database are operational"
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unavailable: {str(e)}"
        )