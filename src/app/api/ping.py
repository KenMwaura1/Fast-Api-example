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
        # Verify database connection if it exists
        db_status = "unknown"
        if hasattr(database, 'is_connected'):
            db_status = "connected" if database.is_connected() else "disconnected"
        
        if db_status == "disconnected":
            return PingResponse(
                status="degraded",
                message="API is running but database connection is unavailable"
            )
        
        return PingResponse(
            status="healthy",
            message="API and database are operational"
        )
    except Exception as e:
        # Return degraded status on error instead of 503
        return PingResponse(
            status="degraded",
            message=f"Health check error: {str(e)}"
        )