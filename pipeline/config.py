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
        "paginated": True,  # Uses fastapi_pagination
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"]
        },
        "primary_key": "user_id",
    },
    "plans": {
        "path": "plans",
        "paginated": False,  # Returns all records
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "plan_id",
    },
    "subscriptions": {
        "path": "subscriptions",
        "paginated": True,  # Uses fastapi_pagination
        "write_disposition": {
            "disposition": "merge",
            "strategy": "scd2",
            "validity_column_names": ["valid_from", "valid_to"]
        },
        "primary_key": "subscription_id",
    },
    "usages": {
        "path": "usages",
        "paginated": True,  # Uses fastapi_pagination
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "usage_id",
    },
    "features": {
        "path": "plan-features",
        "paginated": False,  # Returns all records
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "feature_id",
    },
    "payment_methods": {
        "path": "payment-methods",
        "paginated": False,  # Returns all records
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "payment_method_id",
    },
    "referrals": {
        "path": "referral-sources",
        "paginated": False,  # Returns all records
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "referral_source_id",
    },
    "regions": {
        "path": "regions",
        "paginated": False,  # Returns all records
        "write_disposition": {
            "disposition": "merge",
            "strategy": "upsert"
        },
        "primary_key": "region_id",
    }
}


PARAMS = {
    "username": USERNAME,
    "password": PASSWORD
}