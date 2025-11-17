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
local_db_url = os.environ["LOCAL_DATABASE_URL"]
railway_db_url = os.environ["RAILWAY_DATABASE_URL"]
DATASET_NAME = os.environ["DATASET_NAME"]
PIPELINE_NAME = os.environ["PIPELINE_NAME"]
DESTINATION = os.environ["DESTINATION"]

# Use dlt to load data into Railway
pipeline = dlt.pipeline(
    pipeline_name=PIPELINE_NAME,
    destination=DESTINATION,
    dataset_name=DATASET_NAME,
)

# Connect to local database using psycopg2
local_conn = psycopg2.connect(local_db_url)
local_cur = local_conn.cursor()

tables = ['user', 'plan', 'subscription', 'usage']

for table in tables:
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

local_cur.close()
local_conn.close()

# connect to Railway database to verify using psycopg2
conn = psycopg2.connect(railway_db_url)
cur = conn.cursor()

tables = ['user', 'plan', 'subscription', 'usage']

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM faker_dlt_dataset.{table}")
    result = cur.fetchone()
    
    if result:
        print(f"Table {table} has {result[0]} records in Railway database.")
    else:
        print(f"Table {table} has no records in Railway database.")
    

cur.close()
conn.close()