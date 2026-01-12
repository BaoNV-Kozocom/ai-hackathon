"""
FastAPI routes and endpoints for Laravel Error Analysis Agent.
"""
from fastapi import FastAPI, Request
from typing import Dict, Any
from agent.gpt import ask
import requests
import json
import os
from config.config import LARAVEL_API_URL, PROJECT_API_KEY

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Laravel Error Analysis Agent",
        description="AI-powered error analysis for Laravel applications",
        version="1.0.0"
    )
    
    return app


# Create FastAPI app instance
app = create_app()


@app.post("/analyze-error")
async def analyze_error(request: Request) -> Dict[str, Any]:
    """
    Endpoint to receive error data from Laravel and analyze it.
    It now interacts with the Laravel API to store the error and the analysis.
    """
    # Parse error data from request
    error_data = await request.json()
    
    # Extract error details
    message = error_data.get('message', 'No message')
    file = error_data.get('file', 'Unknown file')
    line = error_data.get('line', 'Unknown line')
    trace = error_data.get('trace', 'No trace available')
    
    # 1. Ingest Log to Laravel
    try:
        ingest_payload = {
            "message": message,
            "level": "error", # Default to error
            "trace": trace,
            "environment": "production" # Default to production
        }
        headers = {
            "X-API-Key": PROJECT_API_KEY,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        print(f"Ingesting log to Laravel: {ingest_payload['message'][:50]}...")
        ingest_response = requests.post(
            f"{LARAVEL_API_URL}/ingest-log",
            json=ingest_payload,
            headers=headers
        )
        
        if ingest_response.status_code >= 400:
             print(f"Failed to ingest log: {ingest_response.text}")
             # Continue with analysis even if storage fails? Or fail?
             # Let's verify: if storage failed, we might not have a thread_id.
             # But let's try to proceed returning analysis to the caller at least.
             thread_id = None
        else:
             ingest_data = ingest_response.json()
             thread_id = ingest_data.get('thread_id')
             print(f"Log ingested. Thread ID: {thread_id}")

    except Exception as e:
        print(f"Error connecting to Laravel API: {e}")
        thread_id = None

    
    # Format the error information for the agent
    error_input = f"""
Laravel Error Report:
====================
Message: {message}
File: {file}
Line: {line}

Stack Trace:
{trace}

Please analyze this error and provide a fix.
"""
    
    # 2. Get AI Analysis
    print(f"Analyzing error...")
    try:
        # Invoke the agent directly
        analysis_result = ask(error_input)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error during AI analysis: {str(e)}"
        }

    # 3. Store AI Response in Laravel
    if thread_id:
        try:
            print(f"Storing AI response for thread {thread_id}...")
            message_payload = {
                "content": analysis_result
            }
            
            store_headers = {
                "X-API-Key": PROJECT_API_KEY,
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            store_response = requests.post(
                f"{LARAVEL_API_URL}/ingest-analysis/{thread_id}",
                json=message_payload,
                headers=store_headers
            )
            
            if store_response.status_code >= 400:
                print(f"Failed to store AI response: {store_response.text}")
            else:
                print("AI response stored successfully.")
            
        except Exception as e:
            print(f"Error storing AI response: {e}")

    return {
        "status": "success",
        "analysis": analysis_result,
        "thread_id": thread_id
    }

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {"status": "healthy"}