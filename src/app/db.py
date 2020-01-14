import os

from sqlalchemy import (Column, DateTime, Integer, String, Table, create_engine, MetaData)
from sqlalchemy.sql import func
from databases import Database


DATABASE_URL = os.getenv("DATABASE_URL")

#SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata - MetaData()

# Databases query builder

database = Database(DATABASE_URL)

