import os

from sqlalchemy import (Column, Integer, String, Table, create_engine, MetaData, Boolean, DateTime)
from sqlalchemy.sql import func
from dotenv import load_dotenv
from databases import Database

load_dotenv()
# Database url if none is passed the default one is used
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://hello_fastapi:hello_fastapi@localhost/hello_fastapi_dev")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("completed", Boolean, default=False),
    Column("created_date", DateTime, default=func.now())
)
# Databases query builder

database = Database(DATABASE_URL)
