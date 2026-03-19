@echo off
echo ==========================================
echo   SAFE PROJECT CREATION
echo ==========================================

set PROJECT_NAME=brainrush_puzzles

IF EXIST %PROJECT_NAME% (
    echo Project already exists. Skipping root creation.
    cd %PROJECT_NAME%
) ELSE (
    mkdir %PROJECT_NAME%
    cd %PROJECT_NAME%
)

echo Creating folders safely...

mkdir src 2>nul
mkdir src\generator 2>nul
mkdir src\renderer 2>nul
mkdir src\uploader 2>nul
mkdir assets 2>nul
mkdir assets\backgrounds 2>nul
mkdir output 2>nul
mkdir output\videos 2>nul
mkdir logs 2>nul

echo Creating files safely...

type nul > app.py
type nul > config.py
type nul > requirements.txt

type nul > src\generator\puzzle_generator.py
type nul > src\renderer\video_renderer.py
type nul > src\uploader\upload_youtube.py

type nul > .env
type nul > build_exe.bat
type nul > run_debug.bat

echo Done without duplication!

pause