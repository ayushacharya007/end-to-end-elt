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
local_db_url = os.getenv("LOCAL_DATABASE_URL")
railway_db_url = os.getenv("RAILWAY_DATABASE_URL")

if not local_db_url:
    raise ValueError("LOCAL_DATABASE_URL environment variable not set")

if not railway_db_url:
    print("RAILWAY_DATABASE_URL environment variable not set")
    raise ValueError("RAILWAY_DATABASE_URL environment variable not set")

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

    # Use dlt to load data into Railway
    pipeline = dlt.pipeline(
        pipeline_name="railway_migration_pipeline",
        destination="postgresql",
        dataset_name="faker_dlt_dataset",
        dev_mode=True,
    )

    # Run the pipeline to load data
    load_info = pipeline.run(table, write_disposition="append")
    print(f"Info: {load_info}")

local_cur.close()
local_conn.close()

# connect to Railway database to verify using psycopg2
conn = psycopg2.connect(railway_db_url)
cur = conn.cursor()

tables = ['user', 'plan', 'subscription', 'usage']

for table in tables:
    cur.execute(f"SELECT COUNT(*) FROM faker_dlt_dataset.{table}")
    result = cur.fetchone()
    count = result[0] if result else 0
    print(f"Table {table} has {count} records.")

cur.close()
conn.close()