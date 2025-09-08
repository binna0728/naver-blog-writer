# Replit 메인 진입점
# web_blog_writer_simple.py를 실행합니다

import subprocess
import sys
import os

if __name__ == "__main__":
    # 환경 변수 설정
    os.environ["STREAMLIT_SERVER_PORT"] = "8080"
    os.environ["STREAMLIT_SERVER_ADDRESS"] = "0.0.0.0"
    os.environ["STREAMLIT_SERVER_HEADLESS"] = "true"
    
    # Streamlit 앱 실행
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", 
        "web_blog_writer_simple.py",
        "--server.port=8080",
        "--server.address=0.0.0.0",
        "--server.headless=true"
    ])