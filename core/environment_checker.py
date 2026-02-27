import subprocess
from utils.logger import get_logger

logger = get_logger(__name__)

import os

class EnvironmentStatus:
    def __init__(self):
        self.git_installed = False
        self.gh_installed = False
        self.gh_authenticated = False
        self.git_path = "git"  # Default to PATH
        self.gh_path = "gh"    # Default to PATH
        self.missing_tools = []

def find_executable(name: str, standard_paths: list[str]) -> str | None:
    """Checks if executable is in PATH or in standard installation folders."""
    # 1. Check if it's in PATH
    try:
        subprocess.run([name, "--version"], capture_output=True, text=True, check=True)
        return name
    except (subprocess.CalledProcessError, FileNotFoundError):
        pass

    # 2. Check standard paths
    for path in standard_paths:
        # Expand environment variables like %LOCALAPPDATA%
        expanded_path = os.path.expandvars(path)
        if os.path.exists(expanded_path):
            try:
                subprocess.run([expanded_path, "--version"], capture_output=True, text=True, check=True)
                return expanded_path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
    return None

def check_environment() -> EnvironmentStatus:
    status = EnvironmentStatus()
    
    # Standard paths for Git on Windows
    git_paths = [
        r"C:\Program Files\Git\bin\git.exe",
        r"C:\Program Files (x86)\Git\bin\git.exe"
    ]
    
    # Standard paths for GitHub CLI on Windows
    gh_paths = [
        r"C:\Program Files\GitHub CLI\gh.exe",
        os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Programs\GitHub CLI\gh.exe"),
        r"C:\Users\Ranz\AppData\Local\Microsoft\WinGet\Links\gh.exe" # Bonus path from previous research
    ]

    # Check Git
    git_exec = find_executable("git", git_paths)
    if git_exec:
        status.git_installed = True
        status.git_path = git_exec
        logger.info(f"Git confirmed at: {git_exec}")
    else:
        status.missing_tools.append("Git")
        logger.error("Git is not installed or not in PATH.")

    # Check GitHub CLI
    gh_exec = find_executable("gh", gh_paths)
    if gh_exec:
        status.gh_installed = True
        status.gh_path = gh_exec
        logger.info(f"GitHub CLI confirmed at: {gh_exec}")
    else:
        status.missing_tools.append("GitHub CLI")
        logger.error("GitHub CLI is not installed or not in PATH.")

    # Check auth if gh is found
    if status.gh_installed:
        try:
            res = subprocess.run([status.gh_path, "auth", "status"], capture_output=True, text=True)
            if res.returncode == 0:
                status.gh_authenticated = True
                logger.info("GitHub CLI is authenticated.")
            else:
                logger.warning("GitHub CLI is not authenticated.")
        except Exception as e:
            logger.error(f"Error checking gh auth status: {e}")

    return status
