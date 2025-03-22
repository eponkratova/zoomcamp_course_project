from typing import Any
import dlt
import requests
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources

@dlt.source(name="custom")
def custom_source() -> Any:
    # Define the configuration for the REST API source.
    config: RESTAPIConfig = {
        "client": {
            "base_url": "http://127.0.0.1:8000",  # Base URL of your FastAPI server
        },
        "resource_defaults": {
            # If your data has a primary key field, you can set it here
            # "primary_key": "id",
            #"write_disposition": "merge",
            "endpoint": {
                # These parameters will be appended to the URL, e.g. ?page=1&page_size=10
                "params": {
                    "page": 1,
                    "page_size": 10,
                },
            },
        },
        "resources": [
            {
                "name": "transaction_details",   # Name of the resource (destination table name)
                "endpoint": "transaction_details",  # Path appended to the base_url (http://127.0.0.1:8000/transaction_details)
            },
        ],
    }
    yield from rest_api_resources(config)


def run_redshift_pipeline() -> None:
    # Create a pipeline that loads data into Redshift.
    pipeline = dlt.pipeline(
        pipeline_name="redshift_pipeline",
        destination="redshift",
#        staging="filesystem",  # Data is staged in the filesystem before being loaded
        dataset_name="transaction_details"
    )
    load_info = pipeline.run(custom_source())
    print("Redshift pipeline load info:", load_info)


def run_s3_pipeline() -> None:
    # Create a pipeline that saves data to the filesystem (which can be later synced to S3 if needed).
    pipeline = dlt.pipeline(
        pipeline_name="s3_pipeline",
        destination="filesystem",
        dataset_name="s3_transaction_details"
    )
    load_info = pipeline.run(custom_source())
    print("Filesystem pipeline load info:", load_info)


if __name__ == "__main__":
    run_redshift_pipeline()
    run_s3_pipeline()