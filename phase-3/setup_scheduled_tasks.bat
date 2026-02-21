@echo off
REM Windows Task Scheduler Setup - Phase 3 CEO Briefing
REM Software Company Style: Automated Scheduled Task Creation

echo ============================================================
echo  CEO BRIEFING - SCHEDULED TASK SETUP
echo  Phase 3 Gold Tier - Automated Configuration
echo ============================================================
echo.

REM Get current directory
set SCRIPT_DIR=%~dp0
set PYTHON_EXE=python
set BRIEFING_SCRIPT=%SCRIPT_DIR%code\generate_ceo_briefing.py

echo [INFO] Script Directory: %SCRIPT_DIR%
echo [INFO] Briefing Script: %BRIEFING_SCRIPT%
echo.

REM Check if Python is available
echo [CHECK] Verifying Python installation...
%PYTHON_EXE% --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found in PATH
    echo [ACTION] Install Python 3.8+ or add to PATH
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Create scheduled task
echo [CREATE] Creating Windows Scheduled Task...
schtasks /create /tn "CEO Briefing - Weekly" /tr "python %BRIEFING_SCRIPT%" /sc weekly /d MON /st 08:00 /ru SYSTEM

if errorlevel 1 (
    echo [WARNING] Task creation failed - may already exist
    echo [INFO] Trying to delete and recreate...
    schtasks /delete /tn "CEO Briefing - Weekly" /f >nul 2>&1
    schtasks /create /tn "CEO Briefing - Weekly" /tr "python %BRIEFING_SCRIPT%" /sc weekly /d MON /st 08:00 /ru SYSTEM
)

echo.
echo [VERIFY] Checking scheduled task...
schtasks /query /tn "CEO Briefing - Weekly" /fo LIST

echo.
echo ============================================================
echo  SETUP COMPLETE
echo ============================================================
echo.
echo Task Name: CEO Briefing - Weekly
echo Schedule: Every Monday at 8:00 AM
echo Run As: SYSTEM
echo.
echo [NEXT] Test manually:
echo   python %BRIEFING_SCRIPT%
echo.
echo [MANAGE] To modify task:
echo   schtasks /change /tn "CEO Briefing - Weekly" /st 09:00
echo.
echo [DELETE] To remove task:
echo   schtasks /delete /tn "CEO Briefing - Weekly" /f
echo.
pause
