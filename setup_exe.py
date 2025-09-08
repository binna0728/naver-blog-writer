"""
실행파일 생성을 위한 setup.py 스크립트
PyInstaller를 사용하여 EXE 파일을 생성합니다.

사용법:
1. 필요한 패키지 설치: pip install pyinstaller
2. 실행파일 생성: python setup_exe.py
"""

import os
import subprocess
import sys

def create_spec_file():
    """PyInstaller spec 파일 생성"""
    spec_content = """
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['gui_블로그자동작성기.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'google.generativeai',
        'google.ai.generativelanguage',
        'selenium',
        'webdriver_manager',
        'openpyxl',
        'pyperclip',
        'tkinter',
        'threading'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='네이버블로그자동작성기',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico' if os.path.exists('icon.ico') else None,
)
"""
    
    with open('블로그자동작성기.spec', 'w', encoding='utf-8') as f:
        f.write(spec_content.strip())
    
    print("✅ spec 파일이 생성되었습니다.")

def install_requirements():
    """필요한 패키지 설치"""
    required_packages = [
        'pyinstaller',
        'google-generativeai',
        'selenium',
        'webdriver-manager',
        'openpyxl', 
        'pyperclip'
    ]
    
    print("📦 필요한 패키지들을 설치합니다...")
    
    for package in required_packages:
        try:
            print(f"설치 중: {package}")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
            print(f"✅ {package} 설치 완료")
        except subprocess.CalledProcessError:
            print(f"❌ {package} 설치 실패")

def create_executable():
    """실행파일 생성"""
    try:
        print("🚀 실행파일 생성을 시작합니다...")
        
        # spec 파일 생성
        create_spec_file()
        
        # PyInstaller 실행
        cmd = [
            'pyinstaller',
            '--onefile',                    # 단일 실행파일
            '--windowed',                   # 콘솔창 숨김
            '--name=네이버블로그자동작성기',    # 실행파일 이름
            '--add-data=geminiapi.py;.',    # geminiapi.py 포함
            '--hidden-import=google.generativeai',
            '--hidden-import=selenium',
            '--hidden-import=webdriver_manager',
            '--hidden-import=openpyxl',
            '--hidden-import=pyperclip',
            'gui_블로그자동작성기.py'
        ]
        
        print("실행 명령어:", ' '.join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 실행파일이 성공적으로 생성되었습니다!")
            print("📁 위치: dist/네이버블로그자동작성기.exe")
            
            # 파일 크기 확인
            exe_path = "dist/네이버블로그자동작성기.exe"
            if os.path.exists(exe_path):
                file_size = os.path.getsize(exe_path) / (1024*1024)  # MB
                print(f"📊 파일 크기: {file_size:.1f} MB")
            
        else:
            print("❌ 실행파일 생성 중 오류가 발생했습니다.")
            print("오류 내용:")
            print(result.stderr)
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def create_simple_executable():
    """간단한 실행파일 생성 (대안)"""
    try:
        print("🔧 간단한 방식으로 실행파일을 생성합니다...")
        
        cmd = [
            'pyinstaller',
            '--onefile',
            '--noconsole',
            'gui_블로그자동작성기.py'
        ]
        
        result = subprocess.run(cmd)
        
        if result.returncode == 0:
            print("✅ 간단한 실행파일이 생성되었습니다!")
            print("📁 위치: dist/gui_블로그자동작성기.exe")
        else:
            print("❌ 실행파일 생성 실패")
            
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

def main():
    print("="*60)
    print("🎯 네이버 블로그 자동 작성기 - 실행파일 생성 도구")
    print("="*60)
    
    # 현재 디렉토리 확인
    print(f"📂 작업 디렉토리: {os.getcwd()}")
    
    # 필요한 파일 확인
    required_files = ['gui_블로그자동작성기.py', 'geminiapi.py']
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ 필수 파일이 없습니다: {file}")
            return
        else:
            print(f"✅ 파일 확인: {file}")
    
    # 패키지 설치
    install_choice = input("\n필요한 패키지를 설치하시겠습니까? (y/n): ").lower()
    if install_choice == 'y':
        install_requirements()
    
    # 실행파일 생성 방식 선택
    print("\n실행파일 생성 방식을 선택하세요:")
    print("1. 고급 설정 (권장)")
    print("2. 간단한 설정")
    
    choice = input("선택 (1/2): ").strip()
    
    if choice == "1":
        create_executable()
    elif choice == "2":
        create_simple_executable()
    else:
        print("잘못된 선택입니다.")
        return
    
    print("\n" + "="*60)
    print("🎉 실행파일 생성 프로세스가 완료되었습니다!")
    print("dist 폴더에서 생성된 exe 파일을 확인하세요.")
    print("="*60)

if __name__ == "__main__":
    main()