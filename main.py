# Replit 메인 진입점
# 완전 자동화 버전을 실행합니다

import subprocess
import sys
import os

if __name__ == "__main__":
    # 환경 변수 설정
    os.environ["STREAMLIT_SERVER_PORT"] = "8080"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Chrome/Selenium 환경 설정
    os.environ["DISPLAY"] = ":99"
    
    # 완전 자동화 Streamlit 앱 실행
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "web_blog_writer_full.py",
        "--server.port=8080",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])