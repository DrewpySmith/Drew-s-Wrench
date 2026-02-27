import subprocess
from typing import Tuple
from utils.logger import get_logger

logger = get_logger(__name__)

class GitHubManager:
    @staticmethod
    def _run_gh_command(args: list[str], cwd: str, gh_exe: str = "gh") -> Tuple[bool, str]:
        try:
            logger.info(f"Running gh command: {gh_exe} {' '.join(args)} in {cwd}")
            result = subprocess.run(
                [gh_exe] + args,
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
                logger.error(f"GitHub CLI command failed: {error_msg}")
                return False, error_msg
        except Exception as e:
            logger.exception(f"Exception during gh subprocess execution: {e}")
            return False, str(e)

    @staticmethod
    def create_repo(repo_path: str, repo_name: str, is_private: bool, gh_exe: str = "gh") -> Tuple[bool, str]:
        visibility = "--private" if is_private else "--public"
        args = ["repo", "create", repo_name, visibility, "--source=.", "--remote=origin"]
        return GitHubManager._run_gh_command(args, repo_path, gh_exe)
