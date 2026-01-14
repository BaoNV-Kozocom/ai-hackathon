import os
from dotenv import load_dotenv

FIXER_TOOLS = [
    {
        "type": "function",
        "name": "search_info",
        "description": "Search the internet for error messages, library documentation, or solutions.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query."
                }
            },
            "required": ["query"]
        }
    },
    {
        "type": "function",
        "name": "read_error_file",
        "description": "Read a specific range of lines from a file to understand context.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Absolute path to the file."
                },
                "line_start": {
                    "type": "integer",
                    "description": "Start line number (1-indexed). Optional. If omitted, reads entire file."
                },
                "line_end": {
                    "type": "integer",
                    "description": "End line number (1-indexed). Optional. If omitted, reads entire file."
                }
            },
            "required": ["file_path"]
        }
    },
    {
        "type": "function",
        "name": "execute_command",
        "description": "Execute a shell command (e.g., grep commands) on ubuntu. Use with caution.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The command to execute."
                }
            },
            "required": ["command"]
        }
    }
]

SYNTHETIC_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads the content of a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the file."},
                    "line_start": {"type": "integer", "description": "Optional start line (1-indexed)."},
                    "line_end": {"type": "integer", "description": "Optional end line (1-indexed)."}
                },
                "required": ["file_path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file_segment",
            "description": "Replaces a specific range of lines in the file with new content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "file_path": {"type": "string", "description": "Absolute path to the file."},
                    "line_start": {"type": "integer", "description": "Start line number (1-indexed)."},
                    "line_end": {"type": "integer", "description": "End line number (1-indexed)."},
                    "new_content": {"type": "string", "description": "The new content to write."}
                },
                "required": ["file_path", "line_start", "line_end", "new_content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "run_syntax_check",
            "description": "Executes a shell command to check syntax.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The syntax check command to execute."}
                },
                "required": ["command"]
            }
        }
    }
]

# Load environment variables
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE")
LARAVEL_API_URL = os.getenv("LARAVEL_API_URL")
PROJECT_API_KEY = os.getenv("PROJECT_API_KEY")

# Backlog Configuration
BACKLOG_BASE_URL = os.getenv("BACKLOG_BASE_URL")
BACKLOG_API_KEY = os.getenv("BACKLOG_API_KEY")
BACKLOG_PROJECT_ID = os.getenv("BACKLOG_PROJECT_ID")
BACKLOG_ISSUE_TYPE_ID = os.getenv("BACKLOG_ISSUE_TYPE_ID")
BACKLOG_PRIORITY_ID = os.getenv("BACKLOG_PRIORITY_ID", "3")

