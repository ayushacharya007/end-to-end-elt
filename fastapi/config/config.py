"""
Configuration for database connections and session management
"""

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")  # provide correct path to your .env file

# Environment variables
RAILWAY_DATABASE_URL = os.environ.get("RAILWAY_DATABASE_URL")
LOCAL_DATABASE_URL = os.environ.get("LOCAL_DATABASE_URL")

if not RAILWAY_DATABASE_URL:
    raise ValueError("RAILWAY_DATABASE_URL environment variable is not set")

if not LOCAL_DATABASE_URL:
    raise ValueError("LOCAL_DATABASE_URL environment variable is not set")

# Create SQLAlchemy engine and session for Railway database
try:
    engine = create_engine(RAILWAY_DATABASE_URL)  # Use Railway database for engine
    # Create a configured "Session" class
    session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise

# TABLE CONFIGURATIONS FOR DLT PIPELINES
TABLE_CONFIGS = {
    # Lookup Tables
    "regions": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["region_id"],
    },
    "referral": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["referral_source_id"],
    },
    "payment_methods": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["payment_method_id"],
    },
    "features": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["feature_id"],
    },    
    "plans": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["plan_id"],
    },
    
    # Transactional Tables
    "users": {
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"],
        },
        "primary_key": ["user_id"],
    },
    "subscriptions": {
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"],
        },
        "primary_key": ["subscription_id"],
    },
    "usage": {
        "write_disposition": {"disposition": "merge", "strategy": "upsert"},
        "primary_key": ["usage_id"],
    },
}