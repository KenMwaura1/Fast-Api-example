from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.api import crud, security
from app.api.models import UserCreate, UserDB, Token, ErrorResponse
from app.db import get_db
from app.config import get_settings

router = APIRouter()
settings = get_settings()


@router.post(
    "/register",
    response_model=UserDB,
    status_code=201,
    responses={400: {"model": ErrorResponse}},
)
async def register(payload: UserCreate, session: AsyncSession = Depends(get_db)):
    """Register a new user"""
    # Check if username already exists
    user = await crud.get_user_by_username(session, payload.username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Check if email already exists
    user = await crud.get_user_by_email(session, payload.email)
    if user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(payload.password)
    await crud.create_user(session, payload, hashed_password)

    # Return user data (without password)
    return await crud.get_user_by_username(session, payload.username)


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    """Login to get access token"""
    user = await crud.get_user_by_username(session, form_data.username)
    if not user or not security.verify_password(
        form_data.password, user["hashed_password"]
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = security.create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
