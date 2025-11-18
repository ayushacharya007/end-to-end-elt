import os
import dlt
from dlt.sources.helpers.rest_client.client import RESTClient
from dlt.sources.helpers.rest_client.auth import HttpBasicAuth
from dotenv import load_dotenv
from config import SOURCES, PARAMS

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# --- Configuration ---
BASE_URL = os.environ["APP_URL"]
DESTINATION = os.environ["ATHENA_DESTINATION"]
PIPELINE_NAME = os.environ["ATHENA_PIPELINE_NAME"]
DATASET_NAME = os.environ["ATHENA_DATASET_NAME"]


# --- DLT Source Definition ---
@dlt.source
def rest_api_source():
    """
    A DLT source that dynamically creates resources for each configured endpoint.
    """
    for source_name, config in SOURCES.items():
        resource_config = {
            "name": source_name,
            "write_disposition": config["write_disposition"],
        }
        if "primary_key" in config:
            resource_config["primary_key"] = config["primary_key"]
            
        yield dlt.resource(
            _get_data(source_name, config),
            **resource_config,
            table_format="iceberg"
        )

def _get_data(source_name, config):
    """
    Fetches data from a specified REST API endpoint.
    """
    print(f"Fetching data for source: {source_name}")
    
    # Use dlt's built-in REST client with basic authentication
    client = RESTClient(
        base_url=BASE_URL,
    )
    
    response = client.get(path=config["path"], params=PARAMS)
    response.raise_for_status()
    
    data = response.json()
    
    # The key in the JSON response is the plural form of the source name (e.g., "users")
    records = data.get(source_name)
    
    if records:
        print(f"Fetched {len(records)} records from {config['path']}")
        yield from records
    else:
        print(f"No records found for {source_name} in the response.")
        # Yield an empty list to handle cases with no data gracefully
        yield []

# --- Pipeline Execution ---

if __name__ == "__main__":
    # Configure the pipeline to load data to the 'postgres' destination
    pipeline = dlt.pipeline(
        pipeline_name=PIPELINE_NAME,
        destination=DESTINATION,
        dataset_name=DATASET_NAME,
    )

    # Run the pipeline with the dynamically created source
    source_instance = rest_api_source()
    load_info = pipeline.run(source_instance)

    # Pretty-print the information on the load outcome
    print(load_info) 