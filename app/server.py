from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Import your existing RAG system
from .main import process_query

app = FastAPI(
    title="Port Tariff Calculator API",
    description="API for calculating port tariffs in South Africa",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class QueryRequest(BaseModel):
    """Model for the query request"""
    query: str

class QueryResponse(BaseModel):
    """Model for the query response"""
    result: str

@app.get("/")
async def root():
    return {"message": "Welcome to Port Tariff Calculator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/calculate", response_model=QueryResponse)
async def calculate_tariffs(request: QueryRequest):
    """
    Calculate port tariffs based on the provided text query.
    
    The query should be in the format:
    "Calculate the different tariffs payable by the following vessel berthing at the port of [port name]: [vessel details]"
    """
    try:
        # Process the query using your existing RAG system
        result = process_query(request.query)
        return QueryResponse(result=result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating tariffs: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app.server:app", host="0.0.0.0", port=8000, reload=True) 