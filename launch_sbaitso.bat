@echo off
REM SBAITSO AI Launcher - Double-click this file to start
REM This batch file launches the PowerShell launcher with proper execution policy

setlocal disabledelayedexpansion

REM Get the directory where this batch file is located
set "scriptDir=%~dp0"

REM Change to the script directory
cd /d "%scriptDir%"

REM Launch the PowerShell script with execution policy bypass
powershell -NoProfile -ExecutionPolicy Bypass -File "%scriptDir%launch_sbaitso.ps1"

REM Keep window open if there was an error
if %ERRORLEVEL% neq 0 (
    echo.
    echo Press any key to close this window...
    pause > nul
)
