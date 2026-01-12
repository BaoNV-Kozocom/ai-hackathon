"""
FastAPI routes and endpoints for Laravel Error Analysis Agent.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from models import analysis_history, AnalysisRecord
from tools import create_agent


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    Returns:
        Configured FastAPI instance
    """
    app = FastAPI(
        title="Laravel Error Analysis Agent",
        description="AI-powered error analysis for Laravel applications",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://127.0.0.1:8000",
            "http://localhost:8000",
            "http://localhost:5173",  # Vite dev server
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app


# Create FastAPI app instance
app = create_app()

# Create agent executor (lazy initialization)
agent_executor = None


def get_agent():
    """Get or create agent executor."""
    global agent_executor
    if agent_executor is None:
        agent_executor = create_agent()
    return agent_executor


@app.post("/analyze-error")
async def analyze_error(request: Request) -> Dict[str, Any]:
    """
    Endpoint to receive error data from Laravel and analyze it using the AI agent.
    
    Request body should contain:
    - message: Error message
    - file: File where error occurred
    - line: Line number
    - trace: Stack trace
    - type: Error type
    - code: Error code
    - timestamp: Error timestamp
    
    Returns:
        Analysis result with status and details
    """
    # Parse error data from request
    error_data = await request.json()
    
    # Extract error details
    message = error_data.get('message', 'No message')
    file = error_data.get('file', 'Unknown file')
    line = error_data.get('line', 'Unknown line')
    trace = error_data.get('trace', 'No trace available')
    error_type = error_data.get('type', 'Unknown error type')
    code = error_data.get('code', 'No code')
    timestamp = error_data.get('timestamp', 'Unknown time')
    
    # Format the error information for the agent
    error_input = f"""
Laravel Error Report:
====================
Type: {error_type}
Message: {message}
File: {file}
Line: {line}
Code: {code}
Timestamp: {timestamp}

Stack Trace:
{trace}

Please analyze this error, read the relevant code, and provide a detailed explanation with suggested fixes.
"""
    
    print("\n" + "="*80)
    print("RECEIVED ERROR FROM LARAVEL")
    print("="*80)
    print(error_input)
    print("="*80 + "\n")
    
    # Get agent executor
    agent = get_agent()
    
    # Invoke the agent
    try:
        result = agent.invoke({"input": error_input})
        analysis = result.get("output", "No analysis generated")
        
        print("\n" + "="*80)
        print("AGENT ANALYSIS")
        print("="*80)
        print(analysis)
        print("="*80 + "\n")
        
        # Create and store the analysis record
        record = AnalysisRecord(
            error_type=error_type,
            error_message=message,
            file=file,
            line=line,
            analysis=analysis,
            error_details=error_data,
            status="success"
        )
        
        analysis_history.add(record)
        
        return {
            "status": "success",
            "analysis": analysis,
            "error_details": error_data,
            "analysis_id": record.id
        }
    
    except Exception as e:
        error_message = f"Error during analysis: {str(e)}"
        print(f"\n{error_message}\n")
        
        # Store failed analysis
        record = AnalysisRecord(
            error_type=error_type,
            error_message=message,
            file=file,
            line=line,
            analysis=error_message,
            error_details=error_data,
            status="error"
        )
        
        analysis_history.add(record)
        
        return {
            "status": "error",
            "message": error_message,
            "error_details": error_data
        }


@app.get("/latest-analysis")
async def get_latest_analysis() -> Dict[str, Any]:
    """
    Endpoint to retrieve the latest error analysis.
    Used by the React frontend to display analysis results.
    
    Returns:
        Latest analysis data or no_data status
    """
    latest = analysis_history.get_latest()
    
    if latest is None:
        return {
            "status": "no_data",
            "message": "No analysis has been performed yet"
        }
    
    return {
        "status": "success",
        "data": latest
    }


@app.get("/analysis-history")
async def get_analysis_history(limit: int = 10) -> Dict[str, Any]:
    """
    Endpoint to retrieve analysis history.
    
    Query parameters:
    - limit: Number of records to return (default: 10, max: 50)
    
    Returns:
        List of analysis records
    """
    history = analysis_history.get_history(limit)
    
    return {
        "status": "success",
        "count": len(history),
        "data": history
    }


@app.get("/")
async def root() -> Dict[str, Any]:
    """
    Root endpoint with API information.
    
    Returns:
        API status and available endpoints
    """
    return {
        "status": "running",
        "message": "Laravel Error Analysis Agent is ready",
        "endpoints": {
            "analyze_error": "POST /analyze-error",
            "latest_analysis": "GET /latest-analysis",
            "analysis_history": "GET /analysis-history?limit=10"
        }
    }


@app.get("/health")
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint.
    
    Returns:
        Health status
    """
    return {
        "status": "healthy",
        "service": "Laravel Error Analysis Agent"
    }
