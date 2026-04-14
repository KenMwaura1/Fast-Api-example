from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    MetaData,
    Boolean,
    DateTime,
    JSON,
    ForeignKey,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.sql import func

from app.config import get_settings

settings = get_settings()

# SQLAlchemy engine and metadata
# Convert "postgresql://" to "postgresql+asyncpg://" if it isn't already
db_url = settings.database_url
if db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

engine = create_async_engine(
    db_url,
    echo=False,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
)
metadata = MetaData()

# Users table for authentication
users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("username", String(50), unique=True, nullable=False, index=True),
    Column("email", String(100), unique=True, nullable=False, index=True),
    Column("hashed_password", String(255), nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("created_date", DateTime, default=func.now(), nullable=False),
)

# Notes table with proper constraints
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(1000), nullable=False),
    Column("completed", Boolean, default=False, nullable=False, index=True),
    Column("is_deleted", Boolean, default=False, nullable=False, index=True),
    Column("tags", JSON, default=[], nullable=False),
    Column("created_date", DateTime, default=func.now(), nullable=False, index=True),
    Column("owner_id", Integer, ForeignKey("users.id"), nullable=False),
)

# Async session maker
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db():
    async with async_session() as session:
        yield session
