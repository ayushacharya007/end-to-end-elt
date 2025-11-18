"""
Configuration for data sources in the ETL pipeline.
"""
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

USERNAME = os.environ["BASIC_AUTH_USERNAME"]
PASSWORD = os.environ["BASIC_AUTH_PASSWORD"]

# Define configurations for each data source
# You can customize the write_disposition, primary_key, etc. for each source.
SOURCES = {
    "users": {
        "path": "users",
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"]
        },
        "primary_key": "user_id",
    },
    "plans": {
        "path": "plans",
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "plan_id",
    },
    "subscriptions": {
        "path": "subscriptions",
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"]
        },
        "primary_key": "subscription_id",
    },
    "usages": {
        "path": "usages",
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "usage_id",
    },
}


PARAMS = {
    "username": USERNAME,
    "password": PASSWORD
}