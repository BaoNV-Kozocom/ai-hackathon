from typing import Dict, Any
from config import config
import re
import os
import ctypes
import subprocess

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
