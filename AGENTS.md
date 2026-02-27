# AI Governance & Architecture Specification

This file defines the strict rules and behavioral constraints for any AI systems (such as coding assistants, LLMs, or autonomous agents) analyzing or modifying this repository.

## MUST DO

- **Preserve secure subprocess execution patterns**: Always pass arguments as a list. Never use `shell=True` for Git or GitHub CLI calls.
- **Maintain structured logging**: Ensure `utils/logger.py` is imported and used to log all executed external commands, failures, and important lifecycle events.
- **Keep UI responsive**: Use `QThread` or appropriate background workers for all I/O or CLI subprocess operations. Never block the PyQt6 main event loop.
- **Follow modular architecture**: Keep GUI code (`gui/`), CLI abstraction logic (`core/`), and general utilities (`utils/`) strictly separated.
- **Preserve environment checks**: Do not remove `core/environment_checker.py`. The application must validate `git`, `gh`, and auth status upon startup.
- **Follow Windows compatibility requirements**: Ensure paths, executable calls, and UI components remain compatible with Windows desktop execution.
- **Maintain type hints and docstrings**: Include type hints for new functions to enforce clarity constraint validations.
- **Respect GitHub CLI authentication model**: Rely on `gh`'s local auth state rather than handling raw tokens.

## MUST NOT DO

- **Remove environment validation**: Do not bypass or remove dependency checks at startup.
- **Store credentials in plaintext**: Do not request, process, or save raw GitHub Personal Access Tokens (PAT) or passwords.
- **Hardcode tokens**: Do not insert API keys or paths into the codebase directly.
- **Introduce unsafe `shell=True` without sanitization**: Avoid `shell=True`. Doing so introduces severe security vulnerabilities in context of Git commands.
- **Execute arbitrary external commands**: Restrict `subprocess` usage exclusively to `git` and `gh` operations.
- **Bypass subprocess error handling**: All subprocess calls must return status flags/data without crashing the main application. Error codes must be surfaced cleanly.
- **Disable logging**: Do not mute or remove `RotatingFileHandler` initialization.
- **Modify security checks**: Do not loosen checks related to `EnvironmentStatus`.
- **Add auto-installation of system software**: Do not write scripts or code to automatically install Git or GitHub CLI. Surface the URLs to the user instead.
- **Introduce telemetry without explicit consent**: Do not introduce analytics trackers, crash reporters, or pingbacks.

## SECURITY PRINCIPLES

1. **Least privilege**: Only run the minimum commands necessary for Git/GitHub workflows.
2. **No credential storage**: Rely solely on secure OS keychains indirectly through GitHub CLI.
3. **Explicit user intent before remote operations**: Push, pull, and create repo must map 1:1 with user clicks.
4. **Safe subprocess usage**: Secure parameter structures only.
5. **Clear error surfacing**: Output stderr streams directly to the log and the UI console securely without exposing sensitive machine info. 

## CODE MODIFICATION POLICY

Any new feature introduced by an AI must:
- **Not break CLI abstraction**: CLI interactions must remain in `core/`.
- **Maintain threading model**: Heavy lifting stays in background workers.
- **Not block GUI thread**: No explicit `sleep` or `subprocess.run` inside `MainWindow` methods aside from invoking worker threads.
- **Include error handling**: Use `try...except` and return proper `Tuple[bool, str]` responses.
- **Include logging**: Detailed error messages inside `app.log`.

## AI CHANGE REVIEW RULES

- AI must **explain reasoning** before proposing major structural changes or refactors to the user.
- AI must **not silently refactor architecture**: Only touch the files asked for by the user.
- AI must **preserve project layout**: Do not flatten directories.
- AI must **not remove AGENTS.md**: This document must persist across all refactors.
