"""
Laravel Error Analysis Agent - Main Entry Point

This application uses LangChain agents to analyze Laravel errors and provide
intelligent debugging assistance.
"""
import os
import uvicorn
from api import app
from models import index_laravel_codebase

# Set OpenAI API key from environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")


@app.on_event("startup")
async def startup_event():
    """Initialize vector store on startup"""
    index_laravel_codebase()


if __name__ == "__main__":
    # Run the FastAPI server on port 5001
    print("Starting Laravel Error Analysis Agent on http://localhost:5001")
    print("Make sure to set OPENAI_API_KEY environment variable")
    uvicorn.run(app, host="0.0.0.0", port=5001)

