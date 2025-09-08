# 🔄 Replit 배포 가이드

## 🚀 Replit으로 배포하기

### 1단계: Replit 계정 생성
1. https://replit.com 접속
2. GitHub 계정으로 로그인

### 2단계: GitHub에서 Import
1. **"Create Repl"** 클릭
2. **"Import from GitHub"** 탭 선택
3. Repository URL 입력: `https://github.com/binna0728/naver-blog-writer`
4. **"Import from GitHub"** 클릭

### 3단계: 자동 설정 확인
Replit이 자동으로 감지하는 파일들:
- ✅ `.replit` - 실행 설정
- ✅ `replit.nix` - 시스템 패키지
- ✅ `requirements.txt` - Python 패키지
- ✅ `main.py` - 메인 실행 파일

### 4단계: 실행
1. **"Run"** 버튼 클릭
2. Replit이 자동으로 패키지 설치
3. Streamlit 앱 실행
4. 웹뷰에서 앱 확인

### 5단계: 배포 (공개)
1. 실행 후 **"Deploy"** 버튼 클릭
2. **"Autoscale"** 선택 (무료)
3. 공개 URL 생성됨

## 🌟 Replit의 장점
- ✅ **완전 무료**: 무제한 사용
- ✅ **브라우저 코딩**: 설치 불필요
- ✅ **즉시 배포**: 클릭 한 번으로 배포
- ✅ **자동 SSL**: HTTPS 자동 적용
- ✅ **실시간 편집**: 코드 수정 즉시 반영
- ✅ **GitHub 연동**: 자동 sync

## 📱 배포 후 사용법
1. Replit에서 생성된 URL 접속
2. 모바일 브라우저에서도 접속 가능
3. Google AI API 키 입력하여 사용

## 🔧 주요 설정 파일들

### `.replit`
```
run = "streamlit run web_blog_writer_simple.py --server.port 8080 --server.address 0.0.0.0"
language = "python3"
entrypoint = "web_blog_writer_simple.py"
```

### `main.py`
```python
import subprocess
import sys

subprocess.run([
    sys.executable, "-m", "streamlit", "run", 
    "web_blog_writer_simple.py",
    "--server.port=8080",
    "--server.address=0.0.0.0"
])
```

## 🛠️ 문제 해결
- **패키지 설치 오류**: Replit이 자동으로 재시도
- **포트 문제**: 8080 포트 고정 사용
- **실행 오류**: Console 탭에서 로그 확인

Replit은 가장 쉽고 빠른 무료 배포 방법입니다! 🎉