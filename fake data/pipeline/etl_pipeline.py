"""
ETL Pipeline for generating and loading fake data

This script orchestrates the generation of all fake data tables
and can load them into a database using DLT.
"""
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
import pandas as pd
import dlt

# Add parent directory to path to allow imports from sibling directories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_generation.generate_users import generate_users
from data_generation.generate_plans import generate_plans
from data_generation.generate_subscriptions import generate_subscriptions
from data_generation.generate_usage import generate_usage


class FakerETL:
    def __init__(self, user_count: int = 1000):
        self.user_count = user_count
        self.data: Dict[str, pd.DataFrame] = {}
        self.pipeline = dlt.pipeline(
            pipeline_name="test_dlt_dataset",
            destination="postgres",
            dataset_name="test_dlt_dataset",
        )

    def extract(self) -> None:
        """
        Generates data in the correct dependency order.
        Stores data in memory (self.data).
        """
        print(f"[{datetime.now()}] Starting data extraction...")

        # 1. Generate Plans (Independent)
        print(f"[{datetime.now()}] Generating Plans...")
        self.data['plans'] = generate_plans()
        
        # 2. Generate Users (Independent)
        print(f"[{datetime.now()}] Generating {self.user_count} Users...")
        self.data['users'] = generate_users(self.user_count)
        
        # 3. Generate Subscriptions (Depends on Users)
        print(f"[{datetime.now()}] Generating Subscriptions...")
        self.data['subscriptions'] = generate_subscriptions(self.data['users'])
        
        # 4. Generate Usage (Depends on Users and Subscriptions)
        print(f"[{datetime.now()}] Generating Usage...")
        self.data['usage'] = generate_usage(self.data['users'], self.data['subscriptions'])
        
        print(f"[{datetime.now()}] Data extraction complete.")

    def load(self) -> None:
        """
        Loads the generated data into the destination using DLT.
        """
        if not self.data:
            print("No data to load. Run extract() first.")
            return

        print(f"[{datetime.now()}] Starting data load...")

        # Load Plans
        # Strategy: upsert (plans are static reference data)
        print(f"[{datetime.now()}] Loading Plans...")
        self.pipeline.run(
            self.data['plans'].to_dict(orient='records'),
            table_name="plans",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="plan_id"
        )

        # Load Users
        # Strategy: scd2 (track changes in user attributes over time)
        print(f"[{datetime.now()}] Loading Users...")
        self.pipeline.run(
            self.data['users'].to_dict(orient='records'),
            table_name="users",
            write_disposition={
                "disposition": "merge", 
                "strategy": "scd2", 
                "validity_column_names": ["valid_from", "valid_to"]
            },
            primary_key="user_id"
        )

        # Load Subscriptions
        # Strategy: scd2 (track subscription status changes)
        print(f"[{datetime.now()}] Loading Subscriptions...")
        self.pipeline.run(
            self.data['subscriptions'].to_dict(orient='records'),
            table_name="subscriptions",
            write_disposition={
                "disposition": "merge", 
                "strategy": "scd2", 
                "validity_column_names": ["valid_from", "valid_to"]
            },
            primary_key="subscription_id"
        )

        # Load Usage
        # Strategy: upsert (load only unique rows)
        print(f"[{datetime.now()}] Loading Usage...")
        self.pipeline.run(
            self.data['usage'].to_dict(orient='records'),
            table_name="usage",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="usage_id"
        )

        print(f"[{datetime.now()}] Data load complete.")

    def run(self):
        """Run the full ETL process"""
        self.extract()
        self.load()


if __name__ == "__main__":
    # Allow configuration via command line or environment variables could be added here
    etl = FakerETL(user_count=10)
    etl.run()