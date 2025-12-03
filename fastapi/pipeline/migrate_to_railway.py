"""
Script to migrate data from local PostgreSQL to Railway PostgreSQL
Run this after adding PostgreSQL to Railway
"""
import os
import sys
import dlt
import psycopg2
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv(dotenv_path="../../.env")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.config import TABLE_CONFIGS

# Environment variables
LOCAL_DB_URL = os.environ.get("LOCAL_DATABASE_URL")
RAILWAY_DB_URL = os.environ.get("RAILWAY_DATABASE_URL")
DATASET_NAME = os.environ.get("RAILWAY_DATASET_NAME", "test_dlt_dataset")
PIPELINE_NAME = os.environ.get("RAILWAY_PIPELINE_NAME", "railway_migration_pipeline")
DESTINATION = os.environ.get("POSTGRES_DESTINATION", "postgres")

if not LOCAL_DB_URL or not RAILWAY_DB_URL:
    raise ValueError("LOCAL_DATABASE_URL and RAILWAY_DATABASE_URL environment variables must be set")

# --- Helper Functions ---
def get_data_from_local_db(cursor, table_name):
    """Fetches all rows from a table and returns them as a list of dictionaries."""
    try:
        # Note: Using test_dlt_dataset schema as per new configuration
        cursor.execute(f"SELECT * FROM {DATASET_NAME}.{table_name}")
        rows = cursor.fetchall()

        if not rows:
            print(f"No data found in table {table_name}, skipping...")
            return None

        if not cursor.description:
            raise ValueError(f"No description available for table {table_name}")

        cols = [desc[0] for desc in cursor.description]
        return [dict(zip(cols, row)) for row in rows]
    except psycopg2.Error as e:
        print(f"Error fetching data from local table {table_name}: {e}")
        return None

def verify_data_in_railway(connection, table_name):
    """Checks and prints the row count of a table in the Railway database."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {DATASET_NAME}.{table_name}")
        result = cursor.fetchone()
        cursor.close()
        connection.commit()  # Commit successful query
        if result:
            print(f"Table '{table_name}' has {result[0]} records in Railway database.")
        else:
            print(f"Table '{table_name}' has no records in Railway database.")
    except Exception as e:
        connection.rollback()  # Rollback on error to prevent transaction abort
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
            print(f"\nProcessing table: {table_name}")
            data = get_data_from_local_db(local_cur, table_name)
            if not data:
                continue

            print(f"Migrating {len(data)} records from table '{table_name}'...")
            
            try:
                load_info = pipeline.run(
                    data,
                    table_name=table_name,
                    write_disposition=config["write_disposition"],
                    primary_key=config["primary_key"],
                )
                print(load_info)
                print(f"Successfully migrated table '{table_name}'.")
            except Exception as e:
                print(f"Failed to migrate table '{table_name}': {e}")

        # --- 2. Verify Data in Railway ---
        print("\nMigration completed. Verifying data in Railway database...")
        railway_conn = psycopg2.connect(RAILWAY_DB_URL)

        for table_name in TABLE_CONFIGS:
            verify_data_in_railway(railway_conn, table_name)
            
        print("\nMigration and verification process finished.")

    except psycopg2.Error as db_error:
        print(f"\nDatabase connection error occurred: {str(db_error)}")
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