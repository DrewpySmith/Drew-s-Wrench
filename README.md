# Drew's Wrench

A production-ready Windows Git client desktop application built with Python and PyQt6. Manage Git repositories and GitHub repositories through a clean, threaded GUI interface.

---

## Features

- Initialize local Git repositories
- Create GitHub repositories via GitHub CLI
- Stage, commit, push, and pull changes
- Real-time console output
- Startup environment validation
- Structured rotating logs
- Background-threaded CLI operations (non-blocking UI)

---

## Setup Instructions

### Prerequisites

| Tool | Install Link |
|------|-------------|
| Python 3.11+ | https://www.python.org/downloads/ |
| Git | https://git-scm.com/downloads |
| GitHub CLI | https://cli.github.com/ |

### GitHub CLI Authentication

After installing GitHub CLI, open a terminal and run:
```bash
gh auth login
```
Follow the interactive prompts to authenticate with your GitHub account. The application relies entirely on this authenticated session.

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

From within the `git_gui_client/` folder:
```bash
python main.py
```

---

## Building the Standalone .exe (Windows)

From within the `git_gui_client/` folder, run:
```bash
build_exe.bat
```

This runs:
```bash
pyinstaller --onefile --windowed --name GitGuiClient --add-data "AGENTS.md;." main.py
```

The compiled executable will be located in:
```
dist/GitGuiClient.exe
```

> **Note:** Git and GitHub CLI must still be installed and accessible in the system PATH when running the compiled .exe.

---

## Directory Structure

```
git_gui_client/
├── main.py                     # Application entry point
├── AGENTS.md                   # AI governance specification
├── build_exe.bat               # Windows build script
├── requirements.txt
├── README.md
│
├── gui/
│   ├── main_window.py          # Main PyQt6 window
│   └── dialogs.py              # QMessageBox wrappers
│
├── core/
│   ├── git_manager.py          # Git CLI wrapper
│   ├── github_manager.py       # GitHub CLI wrapper
│   └── environment_checker.py  # Dependency validator
│
├── utils/
│   └── logger.py               # RotatingFileHandler setup
│
└── logs/
    └── app.log                 # Runtime log output
```

---

## Troubleshooting

### "Git not found" on startup
- Ensure Git is installed: https://git-scm.com/downloads
- Restart the application after installation.
- Verify Git is in your PATH: run `git --version` in a terminal.

### "GitHub CLI not found" on startup
- Install from: https://cli.github.com/
- Restart the application.

### "GitHub CLI not authenticated" warning
- Run `gh auth login` in your terminal and complete the authentication flow.
- Restart the application.

### Push/Pull fails with "no remote" error
- Ensure you have created a GitHub repository first using the **Create GitHub Repo** button before pushing.

### .exe won't run
- Make sure Git and `gh` CLI are both in your PATH environment variable.
- Run from a terminal to see any error output that may be suppressed.

---

## Security Notes

- **No credentials are stored** in the application or its logs.
- All GitHub authentication is managed by GitHub CLI's secure keychain integration.
- Subprocess calls never use `shell=True`.
- All remote operations require an explicit user action (button click).
- See `AGENTS.md` for the full governance and security policy.

---

## Logs

Application logs are stored in `logs/app.log` with automatic rotation (5 MB per file, 5 backups retained). Logs contain command execution records, timestamps, and error details.

# Note
I made this with the help of AI. No I didn't vibe code the entire project because I genuinely want to learn programming as a whole and seeing other projects like 3d renderers, Creating bots, and especially this https://benhoyt.com/writings/pygit/ inspired me to make this. I hope whoever uses this tool help you and probably save the headache of using the CLI. Maybe it's not everyone's fancy of using this and just prefer the CLI, but hey at least it's an option
