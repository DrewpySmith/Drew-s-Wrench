import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QFileDialog, QCheckBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QThread, pyqtSignal

from core.environment_checker import EnvironmentStatus
from core.git_manager import GitManager
from core.github_manager import GitHubManager
from gui.dialogs import show_error
from utils.logger import get_logger

logger = get_logger(__name__)

class WorkerThread(QThread):
    finished = pyqtSignal(bool, str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            success, message = self.func(*self.args, **self.kwargs)
            self.finished.emit(success, message)
        except Exception as e:
            logger.exception("Exception in worker thread")
            self.finished.emit(False, str(e))

class MainWindow(QMainWindow):
    def __init__(self, env_status: EnvironmentStatus):
        super().__init__()
        self.env_status = env_status
        self.worker = None
        self.init_ui()
        self.check_environment_alerts()

    def init_ui(self):
        self.setWindowTitle("Git GUI Client")
        self.resize(700, 500)
        
        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "DrewsWrench.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)

        # Path selector
        path_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText("Select repository path...")
        self.path_input.setReadOnly(True)
        self.browse_btn = QPushButton("Browse")
        self.browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(QLabel("Repository Path:"))
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)
        layout.addLayout(path_layout)

        # Repo Name & Private Toggle
        repo_layout = QHBoxLayout()
        self.repo_name_input = QLineEdit()
        self.repo_name_input.setPlaceholderText("Repository Name (for GitHub)")
        self.private_checkbox = QCheckBox("Private Repository")
        self.private_checkbox.setChecked(True)
        repo_layout.addWidget(QLabel("GitHub Repo Name:"))
        repo_layout.addWidget(self.repo_name_input)
        repo_layout.addWidget(self.private_checkbox)
        layout.addLayout(repo_layout)

        # Commit Message
        commit_layout = QHBoxLayout()
        self.commit_msg_input = QLineEdit()
        self.commit_msg_input.setPlaceholderText("Commit message...")
        commit_layout.addWidget(QLabel("Commit Message:"))
        commit_layout.addWidget(self.commit_msg_input)
        layout.addLayout(commit_layout)

        # Buttons
        button_layout = QHBoxLayout()
        self.init_btn = QPushButton("Initialize Repo")
        self.github_btn = QPushButton("Create GitHub Repo")
        self.commit_btn = QPushButton("Commit")
        self.push_btn = QPushButton("Push")
        self.pull_btn = QPushButton("Pull")

        for btn in [self.init_btn, self.github_btn, self.commit_btn, self.push_btn, self.pull_btn]:
            button_layout.addWidget(btn)

        self.init_btn.clicked.connect(self.on_init)
        self.github_btn.clicked.connect(self.on_github_create)
        self.commit_btn.clicked.connect(self.on_commit)
        self.push_btn.clicked.connect(self.on_push)
        self.pull_btn.clicked.connect(self.on_pull)

        layout.addLayout(button_layout)

        # Output console
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(QLabel("Output Console:"))
        layout.addWidget(self.console)

        # Status label
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)

    def check_environment_alerts(self):
        if self.env_status.missing_tools:
            tools = ", ".join(self.env_status.missing_tools)
            msg = f"The following dependencies are missing: {tools}.\n\n" \
                  f"Git: https://git-scm.com/downloads\n" \
                  f"GitHub CLI: https://cli.github.com/\n\n" \
                  f"Operations will be disabled."
            self.log_output(msg, error=True)
            show_error(self, "Environment Error", msg)
            self.set_buttons_enabled(False)
        elif not self.env_status.gh_authenticated:
            msg = "GitHub CLI is installed but not authenticated. Please run 'gh auth login' in your terminal."
            self.log_output(msg, error=True)
            show_error(self, "Authentication Warning", msg)
            self.github_btn.setEnabled(False)
            self.push_btn.setEnabled(False)
            self.pull_btn.setEnabled(False)

    def browse_path(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Repository Directory")
        if folder:
            self.path_input.setText(folder)
            self.repo_name_input.setText(os.path.basename(folder))

    def log_output(self, message: str, error: bool = False):
        color = "red" if error else "black"
        self.console.append(f"<span style='color:{color}'>{message}</span>")

    def set_buttons_enabled(self, enabled: bool):
        if not self.env_status.missing_tools:
            self.init_btn.setEnabled(enabled)
            self.commit_btn.setEnabled(enabled)
            if self.env_status.gh_authenticated:
                self.github_btn.setEnabled(enabled)
                self.push_btn.setEnabled(enabled)
                self.pull_btn.setEnabled(enabled)

    def start_worker(self, func, *args, **kwargs):
        self.set_buttons_enabled(False)
        self.status_label.setText("Executing...")
        self.worker = WorkerThread(func, *args, **kwargs)
        self.worker.finished.connect(self.on_worker_finished)
        self.worker.start()

    def on_worker_finished(self, success: bool, message: str):
        self.set_buttons_enabled(True)
        self.status_label.setText("Ready")
        if success:
            self.log_output(f"SUCCESS:\n{message}")
        else:
            self.log_output(f"ERROR:\n{message}", error=True)
            show_error(self, "Operation Failed", message)

    def get_repo_path(self) -> str:
        path = self.path_input.text().strip()
        if not path:
            show_error(self, "Error", "Please select a repository path.")
            return ""
        return path

    def on_init(self):
        path = self.get_repo_path()
        if path:
            self.start_worker(GitManager.init, path, self.env_status.git_path)

    def on_github_create(self):
        path = self.get_repo_path()
        repo_name = self.repo_name_input.text().strip()
        if not path or not repo_name:
            show_error(self, "Error", "Please provide a valid path and repository name.")
            return
        is_private = self.private_checkbox.isChecked()
        self.start_worker(GitHubManager.create_repo, path, repo_name, is_private, self.env_status.gh_path)

    def on_commit(self):
        path = self.get_repo_path()
        msg = self.commit_msg_input.text().strip()
        if not path or not msg:
            show_error(self, "Error", "Please provide a valid path and commit message.")
            return
        
        def commit_wrapper(p, m, git_exe):
            success_add, msg_add = GitManager.add_all(p, git_exe)
            if not success_add:
                return False, f"Failed to add files:\n{msg_add}"
            return GitManager.commit(p, m, git_exe)
            
        self.start_worker(commit_wrapper, path, msg, self.env_status.git_path)

    def on_push(self):
        path = self.get_repo_path()
        if path:
            self.start_worker(GitManager.push_origin, path, self.env_status.git_path)

    def on_pull(self):
        path = self.get_repo_path()
        if path:
            self.start_worker(GitManager.pull_origin, path, self.env_status.git_path)
