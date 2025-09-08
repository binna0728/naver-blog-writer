@echo off
echo 네이버 블로그 자동 작성기 EXE 파일 생성 중...
echo.

REM 현재 디렉토리로 이동
cd /d "%~dp0"

REM PyInstaller로 EXE 생성
echo PyInstaller 실행 중...
pyinstaller --onefile ^
    --noconsole ^
    --name "네이버블로그자동작성기" ^
    --exclude-module matplotlib ^
    --exclude-module numpy ^
    --exclude-module scipy ^
    --exclude-module PyQt5 ^
    --exclude-module PyQt6 ^
    --exclude-module pandas ^
    --exclude-module IPython ^
    --exclude-module jupyter ^
    --exclude-module PIL ^
    --exclude-module pygame ^
    --hidden-import google.generativeai ^
    --hidden-import selenium ^
    --hidden-import webdriver_manager ^
    --hidden-import openpyxl ^
    --hidden-import pyperclip ^
    gui_블로그자동작성기.py

echo.
if exist "dist\네이버블로그자동작성기.exe" (
    echo ✅ EXE 파일 생성 성공!
    echo 📁 위치: dist\네이버블로그자동작성기.exe
    
    REM 파일 크기 확인
    for %%A in ("dist\네이버블로그자동작성기.exe") do echo 📊 파일 크기: %%~zA bytes
) else (
    echo ❌ EXE 파일 생성 실패
)

echo.
pause