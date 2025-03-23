from typing import Any
import os
import dlt
import requests
from dlt.common.pendulum import pendulum
from dlt.sources.rest_api import RESTAPIConfig, rest_api_resources


@dlt.source(name="custom")
def custom_source() -> Any:
    """Configurations for the pipeline"""
        config: RESTAPIConfig = {
            "client": {
                "base_url": "https://fastapi-example-ixtk.onrender.com",  #render's API
            },
            "resource_defaults": {
                "endpoint": {
                    "params": {
                        "page": 1,
                        "page_size": 1000,
                    },
                },
            },
            "resources": [
                {
                    "name": "transaction_details",  
                    "endpoint": "transaction_details",  
                },
            ],
        }
        yield from rest_api_resources(config)


def run_redshift_pipeline() -> None:
    """Creading the pipeline"""
    pipeline = dlt.pipeline(
        pipeline_name="redshift_pipeline",
        destination="redshift",
        staging="filesystem",  #dumping the data prior to storing in redshift
        dataset_name="transaction_details"
    )
    load_info = pipeline.run(custom_source())
    print("Redshift pipeline load info:", load_info)


def run_s3_pipeline() -> None:
    """Storing data in s3"""
    pipeline = dlt.pipeline(
        pipeline_name="s3_pipeline",
        destination="filesystem",
        dataset_name="dl_transaction_details"
    )
    load_info = pipeline.run(custom_source())
    print("Filesystem pipeline load info:", load_info)


if __name__ == "__main__":
    run_redshift_pipeline()
    run_s3_pipeline()