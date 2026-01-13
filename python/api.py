
"""
FastAPI routes and endpoints for Laravel Error Analysis Agent.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any
from tools.functions import commit_and_push
import requests
import json
import os
from config.config import LARAVEL_API_URL, PROJECT_API_KEY
from agent.agent_analyzer import agent_analyzer
from agent.agent_fixer import agent_fixer
from agent.agent_synthetic import agent_synthetic

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """
    app = FastAPI(
        title="Laravel Error Analysis Agent",
        description="AI-powered error analysis for Laravel applications",
        version="1.0.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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
             thread_id = None
        else:
             ingest_data = ingest_response.json()
             thread_id = ingest_data.get('thread_id')
             print(f"Log ingested. Thread ID: {thread_id}")

    except Exception as e:
        print(f"Error connecting to Laravel API: {e}")
        thread_id = None

    
    # Helper for storing responses
    def store_agent_response(thread_id, content) -> None:
        if not thread_id:
            return
        try:
            print(f"Storing AI response for thread {thread_id}...")
            message_payload = {
                "content": content
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


    # Format the error information for the agent
    error_log = f"""
Laravel Error Report:
====================
Message: {message}
File: {file}
Line: {line}

Stack Trace:
{trace}
"""
    
    # 2. Get AI Analysis Pipeline
    print(f"Starting AI Pipeline...")
    analysis_data = {}
    fixed_code = ""
    qa_result = ""

    try:
        # --- Step 1: Analyzer ---
        analysis_data = agent_analyzer(error_log)
        
        if "error" in analysis_data:
             error_msg = f"Analysis Failed: {analysis_data['error']}"
             store_agent_response(thread_id, error_msg)
             return {
                 "status": "error",
                 "message": error_msg
             }
        
        # Store Analyzer Summary
        analyzer_summary = (
            f"**Analysis Report**\n"
            f"- **Summary:** {analysis_data.get('error_summary')}\n"
            f"- **File:** `{analysis_data.get('file_path')}:{analysis_data.get('line_number')}`\n"
            f"- **Stack:** {analysis_data.get('language')} / {analysis_data.get('framework')}"
        )
        store_agent_response(thread_id, analyzer_summary)


        # --- Step 2: Fixer ---
        fixed_code = agent_fixer(analysis_data)
        
        # Store Fixer Code
        # fixed_code is now a list of edits
        if isinstance(fixed_code, list):
            fixer_message = f"**Proposed Fixes:**\n```json\n{json.dumps(fixed_code, indent=2)}\n```"
        else:
            fixer_message = f"**Proposed Fix:**\n```\n{fixed_code}\n```"
            
        store_agent_response(thread_id, fixer_message)


        # --- Step 3: Synthetic ---
        qa_result = agent_synthetic(
            analysis_data=analysis_data,
            fixed_code=fixed_code
        )

        # Store Synthetic Result
        store_agent_response(thread_id, f"**Synthesis & Verification Report:**\n{qa_result}")


    except Exception as e:
        error_message = f"Error during AI pipeline: {str(e)}"
        store_agent_response(thread_id, error_message)
        return {
            "status": "error",
            "message": error_message
        }

    return {
        "status": "success",
        "analysis": analysis_data,
        "fixed_code": fixed_code,
        "qa_result": qa_result,
        "thread_id": thread_id
    }

@app.get("/health")
async def health_check() -> Dict[str, Any]:
    return {"status": "healthy"}

@app.post("/commit-code")
async def commit_code(request: Request) -> Dict[str, Any]:
    """
    Endpoint to commit and push code changes.
    Called when user clicks "Commit Code" button in UI.
    """
    data = await request.json()

    issue_name = data.get('issue_name', 'unknown-issue')
    commit_message = data.get('commit_message', 'Fix error via AI debugger')
    files = data.get('files', None)  # Optional: specific files to commit

    print(f"Committing code for issue: {issue_name}")

    result = commit_and_push(issue_name, commit_message, files)

    return result
