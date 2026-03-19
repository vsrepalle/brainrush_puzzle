@echo off
echo ==========================================
echo     PUSHING CODE TO GITHUB
echo ==========================================

REM Navigate to project folder
cd /d %~dp0

REM Initialize git if not already
if not exist ".git" (
    echo [DEBUG] Initializing Git repo...
    git init
)

REM Set remote (force update in case already exists)
echo [DEBUG] Setting remote repository...
git remote remove origin 2>nul
git remote add origin https://github.com/vsrepalle/brainrush_puzzle.git

REM Add all files
echo [DEBUG] Adding files...
git add .

REM Commit
echo [DEBUG] Committing changes...
git commit -m "Auto commit: puzzle automation update"

REM Set branch to main
git branch -M main

REM Push to GitHub
echo [DEBUG] Pushing to GitHub...
git push -u origin main

echo ==========================================
echo     PUSH COMPLETE
echo ==========================================
pause