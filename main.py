# Replit 메인 진입점 - 안정성 우선

import subprocess
import sys
import os

def run_app():
    """앱 실행 함수"""
    try:
        # 환경 변수 설정
        os.environ["STREAMLIT_SERVER_PORT"] = "8080"
        os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
        os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
        
        print("🚀 네이버 블로그 자동 작성기 시작...")
        
        # Streamlit 앱 실행 (안전한 버전 우선)
        try:
            subprocess.run([
                sys.executable, "-m", "streamlit", "run", 
                "web_blog_writer_simple.py",
                "--server.port=8080",
                "--server.address=0.0.0.0",
                "--server.headless=true"
            ])
        except Exception as e:
            print(f"❌ 앱 실행 실패: {e}")
            print("💡 패키지 설치가 필요할 수 있습니다. Shell에서 'pip install -r requirements.txt' 실행하세요.")
            
    except Exception as e:
        print(f"❌ 초기화 실패: {e}")

if __name__ == "__main__":
    run_app()