"""
Configuration for database connections and session management
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")  # provide correct path to your .env file

# Environment variables
LOCAL_DATABASE_URL = os.environ["LOCAL_DATABASE_URL"]
RAILWAY_DATABASE_URL = os.environ["RAILWAY_DATABASE_URL"]

# Create SQLAlchemy engine and session for Railway database
engine = create_engine(RAILWAY_DATABASE_URL)  # Use Railway database for engine

# Create a configured "Session" class
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# TABLE CONFIGURATIONS FOR DLT PIPELINES
TABLE_CONFIGS = {
    "user": {
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"],
        },
        "primary_key": ["user_id"],
    },
    "subscription": {
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"],
        },
        "primary_key": ["user_id", "plan_id"],
    },
    "plan": {
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"],
        },
        "primary_key": ["plan_id"],
    },
    "usage": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["usage_id"],
    },
}