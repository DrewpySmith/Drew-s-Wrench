import subprocess
import os
from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)

class GitManager:
    @staticmethod
    def _run_git_command(args: list[str], cwd: str, git_exe: str = "git") -> Tuple[bool, str]:
        try:
            logger.info(f"Running git command: {git_exe} {' '.join(args)} in {cwd}")
            result = subprocess.run(
                [git_exe] + args,
                cwd=cwd,
                capture_output=True,
                text=True,
                check=False,
                encoding="utf-8"
            )
            if result.returncode == 0:
                logger.info("Command executed successfully.")
                return True, result.stdout.strip()
            else:
                error_msg = result.stderr.strip() or result.stdout.strip()
                logger.error(f"Git command failed: {error_msg}")
                return False, error_msg
        except Exception as e:
            logger.exception(f"Exception during subporcess execution: {e}")
            return False, str(e)

    @staticmethod
    def init(repo_path: str, git_exe: str = "git") -> Tuple[bool, str]:
        return GitManager._run_git_command(["init"], repo_path, git_exe)

    @staticmethod
    def add_all(repo_path: str, git_exe: str = "git") -> Tuple[bool, str]:
        return GitManager._run_git_command(["add", "."], repo_path, git_exe)

    @staticmethod
    def commit(repo_path: str, message: str, git_exe: str = "git") -> Tuple[bool, str]:
        return GitManager._run_git_command(["commit", "-m", message], repo_path, git_exe)

    @staticmethod
    def push_origin(repo_path: str, git_exe: str = "git") -> Tuple[bool, str]:
        success, branch_out = GitManager._run_git_command(["branch", "--show-current"], repo_path, git_exe)
        branch = branch_out if success and branch_out else "main"
        return GitManager._run_git_command(["push", "-u", "origin", branch], repo_path, git_exe)

    @staticmethod
    def pull_origin(repo_path: str, git_exe: str = "git") -> Tuple[bool, str]:
        success, branch_out = GitManager._run_git_command(["branch", "--show-current"], repo_path, git_exe)
        branch = branch_out if success and branch_out else "main"
        return GitManager._run_git_command(["pull", "origin", branch], repo_path, git_exe)
