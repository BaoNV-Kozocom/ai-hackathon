from typing import Dict, Any
import os
import subprocess

def commit_and_push(issue_name: str, commit_message: str, files: list = None) -> Dict[str, Any]:
    """
    Creates a new bugfix branch, commits changes, and pushes to remote.
    Called when user clicks "Commit Code" button in UI.
    """
    print(f"Committing and pushing fix for: {issue_name}")
    try:
        # Generate branch name
        branch_name = f"bugfix/fix-error-{issue_name.lower().replace(' ', '-')[:30]}"

        # Get the project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # 1. Stash any current changes first (in case we're on wrong branch)
        try:
            subprocess.check_output(f"cd {project_root} && git stash", shell=True, stderr=subprocess.STDOUT)
            stashed = True
        except:
            stashed = False

        # 2. Checkout develop
        subprocess.check_output(f"cd {project_root} && git checkout develop", shell=True, stderr=subprocess.STDOUT)

        # 3. Pull latest (optional, but good practice)
        try:
            subprocess.check_output(f"cd {project_root} && git pull origin develop", shell=True, stderr=subprocess.STDOUT)
        except:
            print("Warning: Could not pull from origin develop. Using local.")

        # 4. Create new branch
        try:
            subprocess.check_output(f"cd {project_root} && git checkout -b {branch_name}", shell=True, stderr=subprocess.STDOUT)
        except:
            # Branch might already exist, try to checkout
            subprocess.check_output(f"cd {project_root} && git checkout {branch_name}", shell=True, stderr=subprocess.STDOUT)

        # 5. Apply stashed changes if any
        if stashed:
            try:
                subprocess.check_output(f"cd {project_root} && git stash pop", shell=True, stderr=subprocess.STDOUT)
            except:
                print("Warning: Could not pop stash. Changes might already be applied.")

        # 6. Add files
        if files:
            for file in files:
                subprocess.check_output(f"cd {project_root} && git add {file}", shell=True, stderr=subprocess.STDOUT)
        else:
            subprocess.check_output(f"cd {project_root} && git add -A", shell=True, stderr=subprocess.STDOUT)

        # 7. Commit
        subprocess.check_output(f"cd {project_root} && git commit -m '{commit_message}'", shell=True, stderr=subprocess.STDOUT)

        # 8. Push to remote
        push_result = subprocess.check_output(f"cd {project_root} && git push -u origin {branch_name}", shell=True, stderr=subprocess.STDOUT).decode('utf-8')

        return {
            "status": "success",
            "branch": branch_name,
            "message": f"Changes committed and pushed to branch: {branch_name}",
            "push_output": push_result
        }
    except subprocess.CalledProcessError as e:
        return {"status": "error", "message": f"Git error: {e.output.decode('utf-8')}"}
    except Exception as e:
        return {"status": "error", "message": f"Exception: {str(e)}"}