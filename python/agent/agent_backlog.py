from typing import Dict, Any, Tuple
import requests
import json
import re
from datetime import datetime
from openai import OpenAI
from config.config import (
    LARAVEL_API_URL, 
    PROJECT_API_KEY, 
    OPENAI_API_KEY, 
    BACKLOG_BASE_URL,
    BACKLOG_API_KEY,
    BACKLOG_PROJECT_ID,
    BACKLOG_ISSUE_TYPE_ID,
    BACKLOG_PRIORITY_ID
)


client = OpenAI(api_key=OPENAI_API_KEY)

def agent_backlog(backlog_payload: Dict[str, Any]) -> Tuple[str, str]:
    """
    Parses the Backlog Webhook payload.
    Uses OpenAI with tools to investigate and extract structured error details:
    - message, file, line, trace, code, type, timestamp
    Ingests into Laravel and returns thread_id + formatted log.
    """
    
    # Extract Backlog content
    content = backlog_payload.get('content', {})
    summary = content.get('summary', '')
    description = content.get('description', '')
    
    print(f"Agent Backlog: Analyzing issue '{summary}'...")

    system_prompt = (
        "You are an Advanced Error Log Investigator. "
        "Your goal is to extract specific error details from a Backlog issue description.\n"
        "REQUIRED OUTPUT FORMAT (JSON):\n"
        "{\n"
        "  'message': 'Error message',\n"
        "  'file': '/absolute/path/to/file.php', \n"
        "  'line': <int>, \n"
        "  'trace': 'Stack trace string', \n"
        "  'code': <int or string, error code>, \n"
        "  'type': 'Exception Type (e.g. ValueError)', \n"
        "  'timestamp': 'ISO8601 timestamp (e.g. 2026-01-14T09:30:00Z)' \n"
        "}\n"
        "If exact values are missing, use 'Unknown' or 0."
    )

    user_message = f"Summary: {summary}\n\nDescription:\n{description}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    parsed_data = {}

    try:
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            response_format={"type": "json_object"}
        )
        
        content_text = response.choices[0].message.content or "{}"
        
        # Strip markdown if present
        match = re.search(r"```(?:json)?\n?(.*?)```", content_text, re.DOTALL)
        if match:
            content_text = match.group(1)
            
        try:
            parsed_data = json.loads(content_text)
        except json.JSONDecodeError:
             print("Failed to parse JSON from Backlog Agent. Using raw description related values.")
             parsed_data = {
                 "message": summary,
                 "file": "Unknown",
                 "line": 0,
                 "trace": description
             }

    except Exception as e:
        print(f"Error in Agent Backlog AI Loop: {e}")
        parsed_data = {
                 "message": summary,
                 "file": "Unknown",
                 "line": 0,
                 "trace": description
        }

    # Normalize fields
    message = parsed_data.get('message') or summary
    file = parsed_data.get('file', 'Unknown file')
    line = parsed_data.get('line', 'Unknown line')
    trace = parsed_data.get('trace', 'No trace available')
    code = parsed_data.get('code', 0)
    err_type = parsed_data.get('type', 'Unknown Type')
    timestamp = parsed_data.get('timestamp', datetime.now().isoformat())

    # Format the error information for the agent
    error_log = f"""
Laravel Error Report:
====================
Message: {message}
Type: {err_type}
File: {file}
Line: {line}
Code: {code}
Time: {timestamp}

Stack Trace:
{trace}
"""

    ingest_payload = {
        "message": message,
        "level": "error", 
        "trace": trace,
        "environment": "production",
    }
    
    headers = {
        "X-API-Key": PROJECT_API_KEY,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    print(f"Ingesting structured log to Laravel: {message[:50]}...")
    
    try:
        ingest_response = requests.post(
            f"{LARAVEL_API_URL}/ingest-log",
            json=ingest_payload,
            headers=headers
        )

        if ingest_response.status_code >= 400:
             print(f"Failed to ingest log: {ingest_response.text}")
             return None, error_log
        else:
             ingest_data = ingest_response.json()
             thread_id = ingest_data.get('thread_id')
             print(f"Log ingested. Thread ID: {thread_id}")
             return thread_id, error_log

    except Exception as e:
        print(f"Error connecting to Laravel API: {e}")
        return None, error_log


def create_backlog_issue(error_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new issue in Backlog via API.
    Uses configuration from config.py.
    """
    
    if not BACKLOG_API_KEY or not BACKLOG_PROJECT_ID:
        print("Missing Backlog configuration (API Key or Project ID).")
        return {"error": "Missing Backlog configuration"}

    message = error_data.get('message', 'No message')
    file = error_data.get('file', 'Unknown file')
    line = error_data.get('line', 'Unknown line')
    trace = error_data.get('trace', 'No trace available')
    
    summary = f"Auto-Bug: {message}"
    description = f"""
Auto-generated Bug Report

Message: {message}
File: {file}
Line: {line}

Stack Trace:
{trace}
"""

    payload = {
        "projectId": BACKLOG_PROJECT_ID,
        "summary": summary,
        "issueTypeId": BACKLOG_ISSUE_TYPE_ID,
        "priorityId": BACKLOG_PRIORITY_ID,
        "description": description
    }
    
    url = f"{BACKLOG_BASE_URL}/api/v2/issues?apiKey={BACKLOG_API_KEY}"
    
    try:
        print(f"Creating Backlog issue: {summary}...")
        response = requests.post(url, data=payload) # Backlog API typically accepts form-data or JSON
        
        if response.status_code >= 400:
             print(f"Failed to create Backlog issue: {response.text}")
             return {"error": response.text}
        
        issue_data = response.json()
        print(f"Backlog issue created: {issue_data.get('issueKey')}")
        return issue_data

    except Exception as e:
        print(f"Error creating Backlog issue: {e}")
        return {"error": str(e)}
