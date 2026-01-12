from typing import Dict, Any
from config import config
import re
import os
import ctypes
import subprocess
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
from langchain_community.tools import DuckDuckGoSearchResults

# Initialize Search
wrapper = DuckDuckGoSearchAPIWrapper(region="vi-vi", time="d", max_results=1)
search_tool = DuckDuckGoSearchResults(api_wrapper=wrapper, source="news")

def search_info(query: str) -> Dict[str, Any]:
    print(f"Search info: {query}")
    try:
        # Use the global search_tool
        result = search_tool.invoke(query)
        # Parse the snippet from the result string (LangChain returns a string representation of results)
        # The user's regex suggests the result format contains "snippet: ... title:"
        match = re.search(r"snippet:\s*(.*?)(?=\s*title:|$)", result, re.DOTALL)
        snippet = match.group(1).strip() if match else result # Fallback to full result if regex fails
        return {"status": "success", "result": snippet}

    except Exception as e:
        return {"status": "error", "message": f"Search failed: {str(e)}"}
    except Exception as e:
        return {"status": "error", "message": f"Search failed: {str(e)}"}

def create_fix_branch(issue_name: str) -> Dict[str, Any]:
    """
    Creates a new bugfix branch from develop.
    """
    print(f"Creating fix branch for: {issue_name}")
    try:
        # Generate branch name
        branch_name = f"bugfix/fix-error-{issue_name.lower().replace(' ', '-')[:30]}"
        
        # 1. Checkout develop
        subprocess.check_output("git checkout develop", shell=True, stderr=subprocess.STDOUT)
        
        # 2. Pull latest (optional, but good practice)
        try:
             subprocess.check_output("git pull origin develop", shell=True, stderr=subprocess.STDOUT)
        except:
             print("Warning: Could not pull from origin develop. Using local.")

        # 3. Create new branch
        subprocess.check_output(f"git checkout -b {branch_name}", shell=True, stderr=subprocess.STDOUT)
        
        return {"status": "success", "branch": branch_name, "message": f"Switched to new branch: {branch_name}"}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git error: {e.output.decode('utf-8')}"}
    except Exception as e:
        return {"status": "error", "message": f"Exception: {str(e)}"}
        
def execute_command(command: str) -> Dict[str, Any]:
    print(f"Execute command: {command}")
    try:
        # Execute the command
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT).decode('utf-8')
        return {"status": "success", "output": result}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Command failed: {e.output.decode('utf-8')}"}
    except Exception as e:
        return {"status": "error", "message": f"Exception: {str(e)}"}

def read_error_file(file_path: str, line_start: int, line_end: int) -> Dict[str, Any]:
    print(f"Read error file: {file_path} [{line_start}-{line_end}]")
    try:
        if not os.path.exists(file_path):
             return {"status": "error", "message": f"File not found: {file_path}"}

        # Using sed to read specific lines without loading full file
        cmd = ["sed", "-n", f"{line_start},{line_end}p", file_path]
        result = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode('utf-8')
        
        return {
            "status": "success",
            "content": result,
            "file_path": file_path,
            "range": f"{line_start}-{line_end}"
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Error executing command: {e.output.decode('utf-8')}"}
    except Exception as e:
        return {"status": "error", "message": f"Exception: {str(e)}"}
