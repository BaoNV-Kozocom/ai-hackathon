from typing import Dict, Any
import os
import subprocess

def read_file(file_path: str, line_start: int = None, line_end: int = None) -> str:
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        with open(file_path, "r", encoding="utf-8") as f:
            if line_start is not None and line_end is not None:
                lines = f.readlines()
                # 1-indexed to 0-indexed, slicing handled safely
                start_idx = max(0, line_start - 1)
                end_idx = min(len(lines), line_end)
                return "".join(lines[start_idx:end_idx])
            else:
                return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file_segment(file_path: str, line_start: int, line_end: int, new_content: str) -> str:
    try:
        if not os.path.exists(file_path):
            return f"Error: File not found: {file_path}"
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Safe list slicing (1-indexed input to 0-indexed list)
        # Ensure start is within bounds (min 1 -> min 0)
        start_idx = max(0, line_start - 1)
        # Ensure end is within bounds
        end_idx = min(len(lines), line_end)
        
        if start_idx > len(lines):
                return f"Error: Start line {line_start} is beyond file length {len(lines)}"

        # Prepare new lines
        new_lines_list = new_content.splitlines(keepends=True)
        # Ensure new content ends with newline if original did, or just splitlines might miss it 
        # (splitlines(keepends=True) keeps \n if present in fixed_code)
        # If fixed_code comes from agent without proper newlines, valid.
        
        # Replace logic
        # lines[start_idx:end_idx] replaces the lines from start_idx up to (but not including) end_idx.
        # wait, requirements say line_end is inclusive? Usually line_start to line_end means those lines.
        # Python slicing [start:end] excludes end. So if we want to replace lines 1 to 2 (inclusive), 
        # list indices are 0 and 1. Slice should be [0:2].
        # So end_idx should be line_end.
        
        # However, check if new_content needs to be a list of strings
        new_content_lines = [line + '\n' if not line.endswith('\n') else line for line in new_content.splitlines()]
        if not new_content_lines and new_content: # Handle single line without newline char case if splitlines behaves oddly
                new_content_lines = [new_content + '\n' if not new_content.endswith('\n') else new_content]

        # Actually, let's just use string replacement if we want to be exact, but list replacement is safer for lines.
        lines[start_idx:end_idx] = new_content_lines
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
            
        return "Success: File updated."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def run_syntax_check(command: str) -> str:
    try:
        # Security: In a real env, sanitize command. Here we assume internal agent usage.
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True
        )
        if result.returncode == 0:
            return f"Syntax OK. Output: {result.stdout}"
        else:
            return f"Syntax Error: {result.stderr}"
    except Exception as e:
        return f"Execution Error: {str(e)}"
