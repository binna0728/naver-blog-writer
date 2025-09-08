@echo off
echo 네이버 블로그 자동 작성기 최종 EXE 빌드 시작...
echo.

REM 현재 디렉토리로 이동
cd /d "%~dp0"

REM 기존 빌드 파일 정리
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo 필수 패키지 설치 중...
pip install pyinstaller selenium webdriver-manager google-generativeai openpyxl pyperclip

echo.
echo PyInstaller로 EXE 생성 중...
pyinstaller --onefile ^
    --noconsole ^
    --name "네이버블로그자동작성기" ^
    --icon=blog_icon.ico ^
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
    --hidden-import tkinter ^
    modern_all_in_one.py

echo.
if exist "dist\네이버블로그자동작성기.exe" (
    echo ✅ EXE 파일 생성 성공!
    echo 📁 위치: dist\네이버블로그자동작성기.exe
    
    REM 파일 크기 확인
    for %%A in ("dist\네이버블로그자동작성기.exe") do echo 📊 파일 크기: %%~zA bytes
    
    REM 사용 설명서 복사
    if exist "사용설명서.md" copy "사용설명서.md" "dist\"
    
    echo.
    echo 🎉 빌드 완료! dist 폴더를 확인하세요.
) else (
    echo ❌ EXE 파일 생성 실패
)

echo.
pause