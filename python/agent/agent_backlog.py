from typing import Dict, Any, Tuple
import requests
import json
import re
from datetime import datetime
from openai import OpenAI
from config.config import LARAVEL_API_URL, PROJECT_API_KEY, OPENAI_API_KEY, FIXER_TOOLS
from tools import fixer_functions

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
        "Your goal is to extract specific error details from a Backlog issue description. "
        "You have access to tools to search for files or read code if the description is incomplete.\n"
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
        "If exact values are missing, try to find them using tools (e.g., search for the file). "
        "If still not found, use 'Unknown' or 0."
    )

    user_message = f"Summary: {summary}\n\nDescription:\n{description}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]

    # Tool execution helper (Reuse logic from agent_fixer)
    def handle_tool_call(tool_call):
        name = tool_call.function.name
        try:
            args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
            return {"status": "error", "message": "Invalid JSON arguments"}

        if name == "search_info":
            return fixer_functions.search_info(args["query"])
        if name == "read_error_file":
            return fixer_functions.read_error_file(
                args["file_path"],
                args.get("line_start"),
                args.get("line_end")
            )
        if name == "execute_command":
            return fixer_functions.execute_command(args["command"])
        
        return {"status": "error", "message": f"Tool {name} not supported"}

    parsed_data = {}

    try:
        # 1. Loop for Tool Calls
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            tools=FIXER_TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        
        while response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                print(f"  > Backlog Agent calling tool: {tool_call.function.name}")
                tool_output = handle_tool_call(tool_call)
                
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": str(tool_output)
                })
            
            # Follow-up with tool outputs
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=messages,
                tools=FIXER_TOOLS,
                tool_choice="auto"
            )
            response_message = response.choices[0].message

        # 2. Final Parsing (Ensure JSON)
        content_text = response_message.content or "{}"
        
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
