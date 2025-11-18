"""
Configuration for database connections and session management
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")  # provide correct path to your .env file

LOCAL_DATABASE_URL = os.environ["LOCAL_DATABASE_URL"]
RAILWAY_DATABASE_URL = os.environ["RAILWAY_DATABASE_URL"]

engine = create_engine(RAILWAY_DATABASE_URL)  # Use Railway database for engine

session = sessionmaker(autocommit=False, autoflush=False, bind=engine)