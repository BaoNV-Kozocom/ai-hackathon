"""
Laravel Error Analysis Agent - Main Entry Point
"""
import os
import uvicorn
from api import app
from dotenv import load_dotenv

# Load env
load_dotenv()

if __name__ == "__main__":
    # Run the FastAPI server on port 5001
    print("Starting Laravel Error Analysis Agent on http://localhost:5001")
    uvicorn.run(app, host="0.0.0.0", port=5001)
