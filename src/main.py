from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="AI-Infra Architect API")

@app.get("/")
async def root():
    return {"message": "AI-Infra Architect API is running"}

@app.get("/status")
async def status():
    return {
        "status": "ready",
        "version": "0.1.0",
        "mcp_enabled": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
