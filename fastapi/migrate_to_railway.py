"""
Script to migrate data from local PostgreSQL to Railway PostgreSQL
Run this after adding PostgreSQL to Railway
"""
import os
import dlt
import psycopg2
from dotenv import load_dotenv
from config import TABLE_CONFIGS

# --- Configuration ---
load_dotenv(dotenv_path="../.env")

# Environment variables
LOCAL_DB_URL = os.environ["LOCAL_DATABASE_URL"]
RAILWAY_DB_URL = os.environ["RAILWAY_DATABASE_URL"]
DATASET_NAME = os.environ["RAILWAY_DATASET_NAME"]
PIPELINE_NAME = os.environ["RAILWAY_PIPELINE_NAME"]
DESTINATION = os.environ["POSTGRES_DESTINATION"]

# --- Helper Functions ---
def get_data_from_local_db(cursor, table_name):
    """Fetches all rows from a table and returns them as a list of dictionaries."""
    cursor.execute(f"SELECT * FROM faker_dlt_dataset.{table_name}")
    rows = cursor.fetchall()

    if not rows:
        print(f"No data found in table {table_name}, skipping...")
        return None

    if not cursor.description:
        raise ValueError(f"No description available for table {table_name}")

    cols = [desc[0] for desc in cursor.description]
    return [dict(zip(cols, row)) for row in rows]

def verify_data_in_railway(cursor, table_name):
    """Checks and prints the row count of a table in the Railway database."""
    try:
        cursor.execute(f"SELECT COUNT(*) FROM faker_dlt_dataset.{table_name}")
        result = cursor.fetchone()
        if result:
            print(f"Table '{table_name}' has {result[0]} records in Railway database.")
        else:
            print(f"Table '{table_name}' has no records in Railway database.")
    except Exception as e:
        print(f"Error verifying table '{table_name}': {str(e)}")

# --- Main Execution ---
def main():
    """Main function to run the database migration pipeline."""
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination=DESTINATION,
        dataset_name=DATASET_NAME,
    )

    local_conn = None
    railway_conn = None

    try:
        # --- 1. Extract and Load Data ---
        print("Connecting to local database...")
        local_conn = psycopg2.connect(LOCAL_DB_URL)
        local_cur = local_conn.cursor()
        print("Connected to local database successfully.")

        for table_name, config in TABLE_CONFIGS.items():
            data = get_data_from_local_db(local_cur, table_name)
            if not data:
                continue

            print(f"Migrating {len(data)} records from table '{table_name}'...")
            
            load_info = pipeline.run(
                data,
                table_name=table_name,
                write_disposition=config["write_disposition"],
                primary_key=config["primary_key"],
            )
            print(load_info)
            print(f"Successfully migrated table '{table_name}'.")

        # --- 2. Verify Data in Railway ---
        print("\nMigration completed. Verifying data in Railway database...")
        railway_conn = psycopg2.connect(RAILWAY_DB_URL)
        railway_cur = railway_conn.cursor()

        for table_name in TABLE_CONFIGS:
            verify_data_in_railway(railway_cur, table_name)
            
        print("\nMigration and verification completed successfully!")

    except psycopg2.Error as db_error:
        print(f"\nDatabase error occurred: {str(db_error)}")
        raise
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        raise
    finally:
        # --- 3. Clean up connections ---
        print("\nCleaning up database connections...")
        if local_conn:
            local_conn.close()
            print("Local database connection closed.")
        if railway_conn:
            railway_conn.close()
            print("Railway database connection closed.")

if __name__ == "__main__":
    main()