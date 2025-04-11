from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

app = FastAPI(
    title="Log Classification API",
    description="API for classifying log messages",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Log Classification API is running",
        "endpoints": {
            "classify": "POST /classify/",
            "docs": "GET /docs or /redoc"
        }
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/classify/")
async def classify_logs(file: UploadFile):
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, detail="File must be a CSV")
    
    try:
        df = pd.read_csv(file.file)
        
        if not all(col in df.columns for col in ["source", "log_message"]):
            raise HTTPException(400, detail="CSV requires 'source' and 'log_message' columns")

        # Your classification logic here
        df["target_label"] = classify(list(zip(df["source"], df["log_message"])))
        
        output_file = "output.csv"
        df.to_csv(output_file, index=False)
        return FileResponse(output_file)
        
    except Exception as e:
        raise HTTPException(500, detail=str(e))
    finally:
        file.file.close()

# Make sure to import your classify function
from classify import classify