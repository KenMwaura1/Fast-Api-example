import os

from sqlalchemy import (
    Column, Integer, String, Table, create_engine, MetaData, Boolean, DateTime
)
from sqlalchemy.sql import func
from dotenv import load_dotenv
from databases import Database

load_dotenv()

# Database URL - use environment variable or default
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://hello_fastapi:hello_fastapi@localhost/hello_fastapi_dev"
)

# SQLAlchemy engine and metadata
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Notes table with proper constraints
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("description", String(1000), nullable=False),
    Column("completed", Boolean, default=False, nullable=False),
    Column("created_date", DateTime, default=func.now(), nullable=False)
)

# Async database connection
database = Database(DATABASE_URL)
