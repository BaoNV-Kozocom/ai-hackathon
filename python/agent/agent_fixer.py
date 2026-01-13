from config import config
from openai import OpenAI
from typing import Dict, Any
from tools import fixer_functions
import json
import re

client = OpenAI(api_key=config.OPENAI_API_KEY)

def agent_fixer(analysis_data: Dict[str, Any]) -> list[dict[str, Any]]:
    """
    Generates a fixed code snippet based on the analysis data using OpenAI.
    Supports usage of tools: search_info, read_error_file, execute_command.
    Returns a list of edit operations.
    """
    language = analysis_data.get("language", "Unknown")
    framework = analysis_data.get("framework", "Unknown")
    bad_code = analysis_data.get("bad_code", "")
    error_summary = analysis_data.get("error_summary", "")
    file_path = analysis_data.get("file_path", "")

    system_prompt = f"You are a Senior Expert in {language} and {framework}. Your task is to fix a bug in a {framework} application."

    user_instruction = (
        f"Task: Fix the error: '{error_summary}'\n\n"
        f"File Path: {file_path}\n"
        f"You MUST read the full file using `read_error_file` to understand the context and identify where the error is located.\n"
        f"Also, check if there are any other similar errors or related issues in the file that need to be fixed.\n"
        f"Code Segment context:\n{bad_code}\n\n"
        "IMPORTANT RULES:\n"
        "1. NO LIBRARY MODS: Never modify `vendor/` or `node_modules/`. If the error is there, use `search_info` to find a workaround in user code.\n"
        "2. FIX ALL & DEEP ANALYSIS: You MUST read the full file to identify ALL occurrences of the bug and fix them. Ensure the solution is thorough and correct.\n\n"
        "Return the fix as a JSON Array of objects. Each object represents a replacement.\n"
        "Format:\n"
        "```json\n"
        "[\n"
        "  {\n"
        "    \"line_from\": <start_line>,\n"
        "    \"line_to\": <end_line>,\n"
        "    \"code\": \"<new_code_content>\"\n"
        "  }\n"
        "]\n"
        "```\n"
        "- `line_from` and `line_to` are 1-indexed (inclusive).\n"
        "- Provide multiple objects if you need to edit multiple places (e.g. adding imports).\n"
        "- `code` should be the replacement content. If deleting, provide empty string.\n"
        "- IMPORTANT: Output ONLY the JSON block.\n"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_instruction},
    ]

    def handle_tool_call(tool_call):
        name = tool_call.name
        args = json.loads(tool_call.arguments)

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

    try:
        response = client.responses.create(
            model="gpt-5.1-codex-mini",
            input=messages,
            tools=config.FIXER_TOOLS,
        )

        def get_tool_call(items):
            if not items:
                return None
            for item in items:
                # Handle both object attributes and dictionary access
                item_type = getattr(item, "type", None)
                if not item_type and isinstance(item, dict):
                    item_type = item.get("type")
                
                if item_type == "tool_call" or item_type == "function_call":
                    return item
            return None

        while True:
            # Append all items from the response to messages
            if response.output:
                messages.extend(response.output)
            
            tool_call = get_tool_call(response.output)
            if not tool_call:
                break
                
            tool_result = handle_tool_call(tool_call)

            messages.append({
                "type": "function_call_output",
                "call_id": tool_call.call_id or tool_call.id,
                "output": json.dumps(tool_result),
            })

            response = client.responses.create(
                model="gpt-5.1-codex-mini",
                input=messages,
                tools=config.FIXER_TOOLS,
            )

        content = response.output_text or ""
        
        # Parse JSON output
        match = re.search(r"```(?:json)?\n?(.*?)```", content, re.DOTALL)
        if match:
            content = match.group(1)
            
        try:
            return json.loads(content.strip())
        except json.JSONDecodeError:
            return [{"error": "Failed to parse JSON fix", "raw_content": content}]

    except Exception as e:
        return f"Error detecting fix: {str(e)}"
