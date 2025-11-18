"""
Script to migrate data from local PostgreSQL to Railway PostgreSQL
Run this after adding PostgreSQL to Railway
"""
import os
import dlt
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env") # provide correct path to your .env file

# Local database connection details
LOCAL_DB_URL = os.environ["LOCAL_DATABASE_URL"]
RAILWAY_DB_URL = os.environ["RAILWAY_DATABASE_URL"]
DATASET_NAME = os.environ["DATASET_NAME"]
PIPELINE_NAME = os.environ["PIPELINE_NAME"]
DESTINATION = os.environ["DESTINATION"]

# Use dlt to load data into Railway
pipeline = dlt.pipeline(
    pipeline_name=PIPELINE_NAME,
    destination=DESTINATION,
    dataset_name=DATASET_NAME,
)

# Initialize connection variables
local_conn = None
local_cur = None
conn = None
cur = None

try:
    # Connect to local database using psycopg2
    print("Connecting to local database...")
    local_conn = psycopg2.connect(LOCAL_DB_URL)
    local_cur = local_conn.cursor()
    print("Connected to local database successfully.")

    tables = ['user', 'plan', 'subscription', 'usage']

    for table in tables:
        try:
            local_cur.execute(f"SELECT * FROM faker_dlt_dataset.{table}")
            rows = local_cur.fetchall()
            
            if not rows:
                print(f"No data found in table {table}, skipping...")
                continue
            
            if not local_cur.description:
                raise ValueError(f"No description available for table {table}")
            
            cols = [desc[0] for desc in local_cur.description]
            
            data = [dict(zip(cols, row)) for row in rows]
                
            print(f"Migrating {len(rows)} records from table {table}...")

            
            if table == 'user':
                # Using SCD2 strategy for user table to track changes over time in user data
                load_info = pipeline.run(data, 
                                         table_name=table, 
                                         write_disposition={
                                                "disposition": "merge",
                                                "strategy": "scd2",
                                                "validity_column_names": ["valid_from", "valid_to"]
                                         },
                                         primary_key=['user_id']
                                        )
                print(load_info)
                
            elif table == 'subscription':
                # Using SCD2 strategy for subscription table to track changes over time in subscriptions
                load_info = pipeline.run(data, 
                                         table_name=table, 
                                         write_disposition={
                                                "disposition": "merge",
                                                "strategy": "scd2",
                                                "validity_column_names": ["valid_from", "valid_to"]
                                         },
                                         primary_key=['user_id', 'plan_id']
                                        )
                print(load_info)
                
            elif table == 'plan':
                # Using SCD2 strategy for plan table to track changes over time in plans
                load_info = pipeline.run(data, 
                                         table_name=table, 
                                         write_disposition={
                                                "disposition": "merge",
                                                "strategy": "scd2",
                                                "validity_column_names": ["valid_from", "valid_to"]
                                         },
                                         primary_key=['plan_id']
                                        )
                print(load_info)
                
            elif table == 'usage':
                # Using upsert strategy for usage table as we want to update existing usage records
                load_info = pipeline.run(data, 
                                         table_name=table, 
                                         write_disposition={
                                                "disposition": "merge",
                                                "strategy": "upsert"
                                         },
                                         primary_key=['usage_id']
                                        )
                print(load_info)
            
            print(f"Successfully migrated table {table}.")
            
        except Exception as e:
            print(f"Error migrating table {table}: {str(e)}")
            raise

    print("\nMigration completed. Verifying data in Railway database...")

    # connect to Railway database to verify using psycopg2
    conn = psycopg2.connect(RAILWAY_DB_URL)
    cur = conn.cursor()

    for table in tables:
        try:
            cur.execute(f"SELECT COUNT(*) FROM faker_dlt_dataset.{table}")
            result = cur.fetchone()
            
            if result:
                print(f"Table {table} has {result[0]} records in Railway database.")
            else:
                print(f"Table {table} has no records in Railway database.")
        except Exception as e:
            print(f"Error verifying table {table}: {str(e)}")
    
    print("\nMigration and verification completed successfully!")

except psycopg2.Error as db_error:
    print(f"\nDatabase error occurred: {str(db_error)}")
    raise

except Exception as e:
    print(f"\nUnexpected error occurred: {str(e)}")
    raise

finally:
    # Clean up all connections
    if local_cur:
        try:
            local_cur.close()
            print("\nLocal cursor closed.")
        except Exception as e:
            print(f"Error closing local cursor: {str(e)}")
    
    if local_conn:
        try:
            local_conn.close()
            print("Local connection closed.")
        except Exception as e:
            print(f"Error closing local connection: {str(e)}")
    
    if cur:
        try:
            cur.close()
            print("Railway cursor closed.")
        except Exception as e:
            print(f"Error closing Railway cursor: {str(e)}")
    
    if conn:
        try:
            conn.close()
            print("Railway connection closed.")
        except Exception as e:
            print(f"Error closing Railway connection: {str(e)}")