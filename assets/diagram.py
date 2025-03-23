# generated with https://diagrams.mingrammer.com/docs/getting-started/examples
from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.database import Redshift
from diagrams.onprem.ci import GithubActions
from diagrams.onprem.compute import Server
from diagrams.aws.analytics import Quicksight


with Diagram("Data Pipeline Architecture", show=False, 
             graph_attr={
                 "layout": "neato",
                 "size": "30,30",
                 "dpi": "300",
                 "nodesep": "1.5",
                 "ranksep": "2",
                 "overlap": "false",
                 "splines": "true"
             },
             node_attr={
                 "fontsize": "16",
                 "margin": "1.5,1"
             }):
    # Your nodes and clusters here...

    # Raw data stored in S3
    raw_data = S3("Raw Data (S3)")
    
    # FastAPI service deployed via Render
    fastapi_service = Server("FastAPI (Render)")
    
    # DLT process run via GitHub Actions (using Docker as a proxy icon)
    dlt_process = GithubActions("dlt (GitHub Actions)")
    
    # Processed data destinations:
    # 1. Processed data stored in S3

    with Cluster("Storage"):
        strg_group = [S3("Processed Data (S3)"),
                     Redshift("Redshift (DWH)")]
    
    # Inside Redshift, create views for transformation
    with Cluster("Redshift Views"):
        redshift_views = Redshift("Views")
    
    # Analytics and visualization via Looker Studio (represented by Grafana icon)
    viz = Quicksight("Dashboards with QuickSight")
    
    # Define the pipeline flow
    raw_data >> fastapi_service >> dlt_process
    dlt_process >> strg_group
    strg_group >> redshift_views >> viz

