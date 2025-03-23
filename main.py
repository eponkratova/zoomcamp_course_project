from fastapi import FastAPI, HTTPException, Query
import pandas as pd
import boto3
import io
import os

app = FastAPI()

def load_csv_from_s3():
    """Load CSV from S3"""
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name="us-east-2"
    )
    bucket_name = "zoomcamp-transaction"
    object_key = "raw_data/transaction_data.csv"  

    response = s3.get_object(Bucket=bucket_name, Key=object_key)
    return pd.read_csv(io.BytesIO(response['Body'].read()))

# Load data once at startup and replace NaN with None
df = load_csv_from_s3()
df = df.where(pd.notnull(df), None)

@app.get("/transaction_details")
def get_data(
    page: int = Query(1, ge=1, description="Page number (starting at 1)"),
    page_size: int = Query(100, ge=1, le=1000, description="Number of items per page")
):
    total = len(df)
    start = (page - 1) * page_size
    end = start + page_size

    # If the starting index is beyond the available data, return 404
    if start >= total:
        raise HTTPException(status_code=404, detail="Page not found")

    # Slice the dataframe and convert to a list of records
    data = df.iloc[start:end].to_dict(orient="records")

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "data": data
    }
