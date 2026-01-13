
from config import config
from openai import OpenAI
from typing import Dict, Any, List
import subprocess
import os
import json
from tools import synthetic_functions

client = OpenAI(api_key=config.OPENAI_API_KEY)

def agent_synthetic(analysis_data: Dict[str, Any], fixed_code: List[Dict[str, Any]]) -> str:
    """
    Synthesis Agent.
    1. Receives a list of proposed fixes.
    2. Uses tools (write_file_segment) to apply them.
    3. Runs syntax/lint checks.
    4. Returns a summary.
    """
    # Extract details from analysis data
    file_path = analysis_data.get("file_path", "")
    language = analysis_data.get("language", "Unknown")
    
    # --- Main Agent Logic ---
    
    system_prompt = (
        "You are a DevOps Synthesis Agent. Your goal is to apply a set of approved fixes to a codebase, verify them, and report on the result.\n"
        "You have access to tools to write files and run shell commands.\n\n"
        "Process:\n"
        "1. Analyze the provided 'Fix Plan' (list of edits).\n"
        "2. Execute the fixes using the `write_file_segment` tool for EACH item in the plan. \n"
        "   - IMPORTANT: Execute them in order or in parallel, but ensuring line numbers remain valid.\n"
        "   - Suggestion: The Fix Plan provided is typically careful. But to be safe, if you see multiple edits for the same file, apply them from bottom to top (highest line number first) to avoid shifting issues for earlier lines.\n"
        f"3. After applying fixes, run a syntax check for {language}. Common commands:\n"
        "   - PHP: `php -l {file_path}`\n"
        "   - Python: `python3 -m py_compile {file_path}`\n"
        "   - JavaScript/Node: `node -c {file_path}`\n"
        "4. Return a concise summary of actions and syntax check results."
    )

    # Convert fixed_code list to formatted string if it's a list
    if isinstance(fixed_code, list):
         fixes_str = json.dumps(fixed_code, indent=2)
    else:
         fixes_str = str(fixed_code)

    user_prompt = (
        f"File: {file_path}\n"
        f"Language: {language}\n\n"
        f"Fix Plan (JSON):\n{fixes_str}\n\n"
        "Please apply these fixes using `write_file_segment` and then verify the syntax."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    # Tool execution helper
    def handle_tool_call(tool_call):
        name = tool_call.function.name
        try:
            args = json.loads(tool_call.function.arguments)
        except json.JSONDecodeError:
             return "Error: Invalid JSON arguments"

        if name == "read_file":
            return synthetic_functions.read_file(
                args["file_path"], 
                args.get("line_start"), 
                args.get("line_end")
            )
        elif name == "write_file_segment":
             target_path = args["file_path"]
             # SAFETY CHECK: Do not allow writing to library folders
             if "/vendor/" in target_path or "/node_modules/" in target_path or "site-packages" in target_path:
                 return f"Error: blocked attempt to write to library file '{target_path}'. Please fix the user code instead."

             return synthetic_functions.write_file_segment(
                target_path, 
                args["line_start"], 
                args["line_end"], 
                args["new_content"]
            )
        elif name == "run_syntax_check":
            return synthetic_functions.run_syntax_check(args["command"])
        else:
            return f"Error: Unknown tool {name}"

    try:
        # Initial Call
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=messages,
            tools=config.SYNTHETIC_TOOLS,
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message

        while response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                tool_output = handle_tool_call(tool_call)
                messages.append({
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": tool_call.function.name,
                    "content": str(tool_output)
                })
            
            # Follow-up Call
            response = client.chat.completions.create(
                model="gpt-5-mini",
                messages=messages,
                tools=config.SYNTHETIC_TOOLS,
                tool_choice="auto"
            )
            response_message = response.choices[0].message
            
        return response_message.content or "No response from Synthesis Agent."

    except Exception as e:
        return f"Agent Synthetic Error: {str(e)}"
