@echo off
echo [GitGuiClient] Building standalone Windows .exe with PyInstaller...
echo.

where pyinstaller >nul 2>&1
if errorlevel 1 (
    echo ERROR: PyInstaller is not installed. Please run: pip install pyinstaller
    pause
    exit /b 1
)

pyinstaller --onefile --windowed --name GitGuiClient ^
    --icon "DrewsWrench.ico" ^
    --add-data "AGENTS.md;." ^
    --add-data "DrewsWrench.ico;." ^
    main.py

if errorlevel 1 (
    echo.
    echo BUILD FAILED. Check the output above for errors.
) else (
    echo.
    echo BUILD SUCCESSFUL. Executable is in the dist\ folder.
)

pause
