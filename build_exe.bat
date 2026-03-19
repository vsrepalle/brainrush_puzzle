@echo off
echo ==========================================
echo   BUILDING EXE
echo ==========================================

pip install pyinstaller

pyinstaller --onefile --console app.py

echo DONE. Check dist\app.exe
pause
