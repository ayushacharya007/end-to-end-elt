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

from data_generation.generate_regions import generate_regions
from data_generation.generate_referral_sources import generate_referral_sources
from data_generation.generate_payment_methods import generate_payment_methods
from data_generation.generate_plans import generate_plans
from data_generation.generate_plan_features import generate_plan_features
from data_generation.generate_users import generate_users
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

        # Phase 1: Generate Lookup/Reference Tables (no dependencies)
        print(f"[{datetime.now()}] Generating lookup tables...")
        self.data['regions'] = generate_regions()
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['regions'])} regions")
        
        self.data['referral_sources'] = generate_referral_sources()
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['referral_sources'])} referral sources")
        
        self.data['payment_methods'] = generate_payment_methods()
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['payment_methods'])} payment methods")
        
        self.data['plans'] = generate_plans()
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['plans'])} plans")
        
        self.data['plan_features'] = generate_plan_features()
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['plan_features'])} plan features")
        
        # Phase 2: Generate Transactional Tables (have dependencies)
        print(f"[{datetime.now()}] Generating transactional tables...")
        
        self.data['users'] = generate_users(self.user_count)
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['users'])} users")
        
        self.data['subscriptions'] = generate_subscriptions(self.data['users'])
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['subscriptions'])} subscriptions")
        
        self.data['usage'] = generate_usage(self.data['users'], self.data['subscriptions'])
        print(f"[{datetime.now()}] ✓ Generated {len(self.data['usage'])} usage records")
        
        print(f"[{datetime.now()}] Data extraction complete.")

    def load(self) -> None:
        """
        Loads the generated data into the destination using DLT.
        Loads in dependency order: lookup tables first, then transactional tables.
        """
        if not self.data:
            print("No data to load. Run extract() first.")
            return

        print(f"[{datetime.now()}] Starting data load...")

        # === PHASE 1: Load Lookup/Reference Tables ===
        print(f"[{datetime.now()}] Loading lookup tables...")
        
        # Regions
        print(f"[{datetime.now()}] Loading regions...")
        self.pipeline.run(
            self.data['regions'].to_dict(orient='records'),
            table_name="regions",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="region_id"
        )
        
        # Referral Sources
        print(f"[{datetime.now()}] Loading referral_sources...")
        self.pipeline.run(
            self.data['referral_sources'].to_dict(orient='records'),
            table_name="referral",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="referral_source_id"
        )
        
        # Payment Methods
        print(f"[{datetime.now()}] Loading payment_methods...")
        self.pipeline.run(
            self.data['payment_methods'].to_dict(orient='records'),
            table_name="payment_methods",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="payment_method_id"
        )
        
        # Plans
        print(f"[{datetime.now()}] Loading plans...")
        self.pipeline.run(
            self.data['plans'].to_dict(orient='records'),
            table_name="plans",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="plan_id"
        )
        
        # Plan Features
        print(f"[{datetime.now()}] Loading plan_features...")
        self.pipeline.run(
            self.data['plan_features'].to_dict(orient='records'),
            table_name="features",
            write_disposition={"disposition": "merge", "strategy": "upsert"},
            primary_key="feature_id"
        )

        # === PHASE 2: Load Transactional Tables ===
        print(f"[{datetime.now()}] Loading transactional tables...")
        
        # Users
        print(f"[{datetime.now()}] Loading users...")
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

        # Subscriptions
        print(f"[{datetime.now()}] Loading subscriptions...")
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

        # Usage
        print(f"[{datetime.now()}] Loading usage...")
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