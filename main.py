from fastapi import FastAPI, HTTPException, Query
import pandas as pd

app = FastAPI()

# Load CSV and handle NaN values for JSON compatibility
df = pd.read_csv("D:/OneDrive/Documents/zoomcamp/transaction_data.csv")
df = df.where(pd.notnull(df), None)

@app.get("/transaction_details") #type of the http request
def get_data( 
    page: int = Query(1, ge=1, description="Page number (starting at 1)"),
    page_size: int = Query(100, ge=1, le=10, description="Number of items per page") #num of items from 1 to 1000
):
    total = len(df)
    start = (page - 1) * page_size
    end = start + page_size
    if start >= total:
        raise HTTPException(status_code=404, detail="No data found") #loops throughout the pages and throws the error if the data is not found
    page_data = df.iloc[start:end].to_dict(orient="records") #return .json objects
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "data": page_data
    }