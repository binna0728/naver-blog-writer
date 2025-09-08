# 🚀 네이버 블로그 자동 작성기 - Streamlit Cloud 배포

## 📋 배포 준비 파일들

### 필수 파일들:
- `web_blog_writer.py` - 메인 웹 앱
- `geminiapi.py` - Google AI API 모듈  
- `requirements.txt` - Python 패키지 의존성
- `packages.txt` - 시스템 패키지 (Chrome 브라우저)
- `.streamlit/config.toml` - Streamlit 설정

## 🌐 Streamlit Cloud 배포 방법

### 1단계: GitHub 리포지토리 생성
1. GitHub에서 새 리포지토리 생성
2. 다음 파일들을 업로드:
   ```
   web_blog_writer.py
   geminiapi.py
   requirements.txt
   packages.txt
   .streamlit/config.toml
   README_DEPLOY.md
   ```

### 2단계: Streamlit Cloud 배포
1. https://share.streamlit.io/ 접속
2. GitHub 계정으로 로그인
3. "New app" 클릭
4. 리포지토리 선택
5. Main file: `web_blog_writer.py`
6. Deploy 클릭

### 3단계: 환경 변수 설정 (선택사항)
- Advanced settings에서 환경 변수 추가 가능
- 보안이 중요한 API 키 등을 환경 변수로 관리

## ⚠️ 주의사항

### Selenium 제약
- Streamlit Cloud는 제한된 환경에서 Selenium이 실행됩니다
- 헤드리스 모드 필수
- 일부 기능이 제한될 수 있습니다

### 대안 방법
만약 Selenium이 정상 동작하지 않으면:
1. **Heroku** - 더 유연한 환경
2. **Railway** - 최신 플랫폼  
3. **Render** - Heroku 대안

## 🔧 로컬 테스트
```bash
pip install -r requirements.txt
streamlit run web_blog_writer.py
```

## 📱 모바일 최적화
- 반응형 디자인 적용
- 다크 테마 지원
- 터치 친화적 UI