import os
import dlt
from dlt.sources.helpers.rest_client.client import RESTClient
from dlt.sources.helpers.rest_client.paginators import PageNumberPaginator
from dotenv import load_dotenv
from config import SOURCES, PARAMS
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException
from datetime import datetime

# Load environment variables from .env file
load_dotenv(dotenv_path="../.env")

# --- Configuration ---
BASE_URL = os.getenv("APP_URL")
DESTINATION = os.getenv("ATHENA_DESTINATION")
PIPELINE_NAME = os.getenv("ATHENA_PIPELINE_NAME")
DATASET_NAME = os.getenv("ATHENA_DATASET_NAME")

# Validate required environment variables
if BASE_URL is None or DESTINATION is None or PIPELINE_NAME is None or DATASET_NAME is None:
    raise ValueError(
        "Missing required environment variables. Ensure APP_URL, ATHENA_DESTINATION, "
        "ATHENA_PIPELINE_NAME, and ATHENA_DATASET_NAME are set."
    )


# --- DLT Source Definition ---
@dlt.source
def rest_api_source():
    """
    A DLT source that dynamically creates resources for each configured endpoint.
    Handles both paginated and non-paginated endpoints based on configuration.
    """
    for source_name, config in SOURCES.items():
        resource_config = {
            "name": source_name,
            "write_disposition": config["write_disposition"],
            "primary_key": config.get("primary_key", None)
        }
        
        yield dlt.resource(
            _get_data(source_name, config),
            **resource_config,
            table_format="iceberg"
        )


def _get_data(source_name, config):
    """
    Fetches data from a specified REST API endpoint.
    Handles both paginated and non-paginated endpoints with comprehensive error handling.
    
    Args:
        source_name: Name of the data source
        config: Configuration dictionary containing path, pagination flag, etc.
    
    Yields:
        Records from the API endpoint
    """
    is_paginated = config.get("paginated", False)
    
    try:
        # Configure REST client with appropriate paginator
        if is_paginated:
            paginator = PageNumberPaginator(
                base_page=1,
                page_param="page",
                total_path="total"
            )
        else:
            paginator = None
        
        client = RESTClient(
            base_url=BASE_URL,  # type: ignore[arg-type]
            paginator=paginator,
        )
        
        try:
            if is_paginated:
                # Add page size to params for paginated endpoints
                paginated_params = {**PARAMS, "size": 100}
                
                pages = client.paginate(
                    path=config["path"],
                    params=paginated_params,
                    data_selector="items"
                )
                
                # Iterate through pages
                record_count = 0
                page_count = 0
                for page in pages:
                    if page:
                        page_count += 1
                        record_count += len(page)
                        yield from page
                
                print(f"✓ Fetched {record_count} records from {page_count} page(s) for {source_name}")
            else:
                response_obj = client.get(config["path"], params=PARAMS)
                
                try:
                    response = response_obj.json()
                except Exception as json_error:
                    print(f"✗ Failed to parse JSON response for {source_name}: {json_error}")
                    raise
                
                if not isinstance(response, dict):
                    print(f"⚠ Unexpected response type for {source_name}: {type(response)}")
                    return
                
                # Check if response contains items
                if "items" in response:
                    items = response["items"]
                    if items:
                        print(f"✓ Fetched {len(items)} records for {source_name}")
                        yield from items
                    else:
                        print(f"⚠ No records found for {source_name}")
                elif "message" in response:
                    print(f"{source_name}: {response['message']}")
                else:
                    print(f"⚠ Unexpected response structure for {source_name}")
                    
        except HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else None
            
            if status_code == 401:
                print(f"✗ Authentication failed for {source_name}. Check credentials.")
            elif status_code == 403:
                print(f"✗ Access forbidden for {source_name}. Insufficient permissions.")
            elif status_code == 404:
                print(f"✗ Endpoint not found for {source_name}: /{config['path']}")
            elif status_code == 500:
                print(f"✗ Server error for {source_name}. The API may be experiencing issues.")
            else:
                print(f"✗ HTTP error {status_code} for {source_name}: {str(e)}")
            raise
            
        except ConnectionError as e:
            print(f"✗ Connection error for {source_name}: {str(e)}")
            print(f"  Check if the API server is running at {BASE_URL}")
            raise
            
        except Timeout as e:
            print(f"✗ Request timeout for {source_name}: {str(e)}")
            raise
            
        except RequestException as e:
            print(f"✗ Request exception for {source_name}: {str(e)}")
            raise
            
    except Exception as e:
        print(f"✗ Unexpected error processing {source_name}: {str(e)}")
        raise


# --- Pipeline Execution ---

if __name__ == "__main__":
    print("=" * 60)
    print(f"Starting pipeline run at {datetime.now()}")
    print("=" * 60)
    
    try:
        pipeline = dlt.pipeline(
            pipeline_name=PIPELINE_NAME,
            destination=DESTINATION,
            dataset_name=DATASET_NAME
        )
        
        source = rest_api_source()
        info = pipeline.run(source)
        print(info)
        
    except Exception as e:
        print(f"✗ Pipeline failed: {str(e)}")
        raise
        
    finally:
        print(f"Pipeline completed at {datetime.now()}")
