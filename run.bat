@echo off
REM Generate facets from Claude Code session-meta files
REM Usage: run.bat

echo.
echo ============================================
echo  Generating Facets from Session-Meta Files
echo ============================================
echo.

python %~dp0impl.py

echo.
pause
