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
            "description": "Execute a shell command to fix errors or perform actions. Only use for file modifications (sed, echo, etc). DO NOT use for git commands.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The shell command to execute (NO git commands allowed)"}
                },
                "required": ["command"],
            },
        },
    },
]

SYSTEM_PROMPT = """You are a specialized debugging assistant for Laravel applications.
Your goal is to analyze the provided error report, read the relevant code files, AND AUTOMATICALLY FIX THE ISSUE LOCALLY using `execute_command`.
You are an AUTONOMOUS AGENT. You must not just describe the fix, you MUST APPLY IT to the local files.

IMPORTANT RULES:
- DO NOT use any git commands (no git add, git commit, git push, git checkout, git branch, etc.)
- Only modify the source files directly using sed, echo, or similar file editing commands
- The user will manually commit and push the changes later via the UI

You must return your response in the following JSON format:
{
    "analysis": "Brief explanation of the root cause.",
    "solution": "Description of the fix.",
    "files_modified": ["List of files that were modified"],
    "command": "The exact shell command used to apply the fix."
}

Use the `read_error_file` tool to inspect code.
Use the `search_info` tool if you don't know how to fix the error or need external information.
Use `execute_command` to apply fixes (sed/write) and verify - BUT NO GIT COMMANDS.
YOU MUST EXECUTE THE COMMANDS TO FIX THE CODE. DO NOT STOP AT ANALYSIS.
If you need to verify the fix, you can run php artisan commands via `execute_command`.
"""
# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE")
LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
PROJECT_API_KEY = os.getenv("PROJECT_API_KEY")

