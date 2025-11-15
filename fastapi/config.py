from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

LOCAL_DATABASE_URL = os.getenv("LOCAL_DATABASE_URL")
RAILWAY_DATABASE_URL = os.getenv("RAILWAY_DATABASE_URL")

if LOCAL_DATABASE_URL is None:
    raise ValueError("LOCAL_DATABASE_URL environment variable must be set")

if RAILWAY_DATABASE_URL is None:
    raise ValueError("RAILWAY_DATABASE_URL environment variable must be set")

engine = create_engine(RAILWAY_DATABASE_URL)  # Use Railway database for engine

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)