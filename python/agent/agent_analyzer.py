
import json
from config import config
from openai import OpenAI
from typing import Dict, Any
from tools.analyzer_functions import read_error_file

client = OpenAI(api_key=config.OPENAI_API_KEY)

def agent_analyzer(error_log: str) -> Dict[str, Any]:
    """
    Analyzes an error log, parses it with OpenAI, and fetches the relevant code snippet.
    Also detects the technology stack (Language & Framework).
    """
    try:
        # Step 1: AI Analysis (Enhanced)
        response = client.chat.completions.create(
            model="gpt-5-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an Error & Tech Stack Analyzer. "
                        "Analyze the provided Error Log and Stack Trace. "
                        "Identify the programming language (e.g., PHP, Python, TypeScript) and the specific framework (e.g., Laravel, Django, Next.js, FastApi). "
                        "Look for namespaces, file extensions, and path structures as clues.\n"
                        "Check if the error comes from a third-party library (e.g., 'vendor/', 'node_modules/'). "
                        "If it does, try to find the last line of USER CODE in the stack trace that triggered the error. "
                        "However, if the error is internal to the library, identifying the library file is also acceptable.\n\n"
                        "Return a JSON object:\n"
                        "{\n"
                        "  'file_path': 'path/to/file',\n"
                        "  'line_number': <int>,\n"
                        "  'context_start': <int, line_number - 5>,\n"
                        "  'context_end': <int, line_number + 5>,\n"
                        "  'language': 'The identified language (e.g., PHP)',\n"
                        "  'framework': 'The identified framework (e.g., Laravel 10) or None',\n"
                        "  'summary': 'Brief error description',\n"
                        "  'is_library_file': <bool> // True if file_path is in vendor, node_modules, etc.\n"
                        "}"
                    ),
                },
                {"role": "user", "content": error_log},
            ],
            response_format={"type": "json_object"},
            stream=False,
        )

        content = response.choices[0].message.content
        if not content:
            return {"error": "Empty response from OpenAI"}

        # Step 2: JSON Parsing
        analysis_result = json.loads(content)
        
        file_path = analysis_result.get("file_path")
        line_number = analysis_result.get("line_number")
        context_start = analysis_result.get("context_start")
        context_end = analysis_result.get("context_end")
        error_summary = analysis_result.get("summary")
        language = analysis_result.get("language", "Unknown")
        framework = analysis_result.get("framework", "Unknown")
        is_library_file = analysis_result.get("is_library_file", False)

        if not file_path or line_number is None:
             return {"error": "Incomplete analysis from OpenAI"}

        # Step 3: Fetch Context
        file_data = read_error_file(file_path, context_start, context_end)
        
        bad_code = ""
        if file_data.get("status") == "success":
            bad_code = file_data.get("content", "")
        else:
            return {"error": f"Could not read file: {file_data.get('message')}"}

        # Step 4: Output
        return {
            "file_path": file_path,
            "line_number": line_number,
            "bad_code": bad_code,
            "language": language,
            "framework": framework,
            "error_summary": error_summary,
            "context_start": context_start,
            "context_end": context_end,
            "full_log": error_log,
            "is_library_file": is_library_file,
        }

    except json.JSONDecodeError:
        return {"error": "Failed to parse JSON response from OpenAI"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
