import os
from dotenv import load_dotenv

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_info",
            "description": "Search external or factual information (using DuckDuckGo) when the user asks a question that requires looking something up or when the error is difficult.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_fix_branch",
            "description": "Create a new git branch from 'develop' to start fixing a bug. MUST BE USED before applying any fixes.",
            "parameters": {
                "type": "object",
                "properties": {"issue_name": {"type": "string", "description": "Short description of the issue (e.g., 'null-pointer', 'user-login')"}},
                "required": ["issue_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "read_error_file",
            "description": "Read a specific range of lines from a file using a system command (sed). Useful for checking error logs or code snippets without loading the full file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Path to the file to read"},
                    "line_start": {"type": "integer", "description": "Start line number (inclusive)"},
                    "line_end": {"type": "integer", "description": "End line number (inclusive)"}
                },
                "required": ["file_path", "line_start", "line_end"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "execute_command",
            "description": "Execute a shell command found in the chat to fix errors or perform actions. Use this when the user asks to run a command or fix a file via command.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute"}
                },
                "required": ["command"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a specialized debugging assistant for Laravel applications.
Your goal is to analyze the provided error report, read the relevant code files, AND AUTOMATICALLY FIX THE ISSUE using `execute_command`.
You are an AUTONOMOUS AGENT. You must not just describe the fix, you MUST APPLY IT.

You must return your response in the following JSON format:
{
    "analysis": "Brief explanation of the root cause.",
    "solution": "Description of the fix.",
    "command": "The exact shell command to apply the fix (e.g., sed -i ... or other bash commands)."
}

Use the `read_error_file` tool to inspect code.
Use the `search_info` tool if you don't know how to fix the error or need external information.
Before applying any file modifications, you MUST use `create_fix_branch` to switch to a new branch.
Then use `execute_command` to apply fixes (sed/write) and verify.
YOU MUST EXECUTE THE COMMANDS TO FIX THE CODE. DO NOT STOP AT ANALYSIS.
If you need to verify the fix, you can run php artisan commands via `execute_command`.
"""
# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE")
LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
PROJECT_API_KEY = os.getenv("PROJECT_API_KEY")

