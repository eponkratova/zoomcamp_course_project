from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import boto3
import io
import os

app = FastAPI()

def load_csv_from_s3():
    """The function loads CSV from S3"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-2"
    )
    bucket_name = "zoomcamp-transaction"
    object_key = "transaction_data.csv"  

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return pd.read_csv(io.BytesIO(response['Body'].read()))

# Load once on startup
df = load_csv_from_s3()
df = df.where(pd.notnull(df), None)

@app.get("/transaction_details")
def get_data(
    page: int = Query(1, ge=1, description="Page number (starting at 1)"),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page")
):
    total = len(df)
    start = (page - 1) * page_size
    end = start + page
