@echo off
REM Launch script for FilesystemWatcher (Phase 1)
REM This script starts the filesystem watcher to monitor the test drop folder

echo ========================================
echo FilesystemWatcher - Phase 1
echo ========================================
echo.
echo Vault Path: C:\Users\User\Desktop\hakathon-00\AI_Employee_Vault
echo Watch Directory: C:\Users\User\Desktop\hakathon-00\test_drop_folder
echo.
echo Starting watcher... Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python filesystem_watcher.py

pause
