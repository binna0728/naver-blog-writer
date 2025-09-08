# 🚀 Replit 완전 자동화 가이드

## 📋 단계별 설정 방법

### 1단계: Replit Import
1. https://replit.com 접속
2. "Create Repl" → "Import from GitHub"
3. URL: `https://github.com/binna0728/naver-blog-writer`
4. "Import from GitHub" 클릭

### 2단계: Chrome 설치 (필수)
Replit Shell에서 다음 명령어 실행:
```bash
bash setup.sh
```

### 3단계: 앱 실행
```bash
python main.py
```

## 🛠️ 문제 해결

### Chrome 설치 오류가 발생하는 경우:
```bash
# 수동 Chrome 설치
sudo apt-get update
sudo apt-get install -y chromium-browser
sudo apt-get install -y chromium-chromedriver
```

### 드라이버 오류가 발생하는 경우:
```bash
# 환경 변수 설정
export DISPLAY=:99
export CHROME_BIN=/usr/bin/chromium-browser
export CHROMEDRIVER_PATH=/usr/bin/chromedriver
```

### 포트 오류가 발생하는 경우:
```bash
# 포트를 변경해서 실행
streamlit run web_blog_writer_full.py --server.port 8080 --server.address 0.0.0.0
```

## ✨ 사용법

### 1. 계정 설정
- 사이드바에서 네이버 아이디/비밀번호 입력
- Google AI API 키 입력
- 각각 테스트 버튼으로 확인

### 2. 포스트 생성
- 키워드 입력 (예: "맛집", "여행")
- 포스트 수 선택 (1-10개)
- 글쓰기 스타일 선택
- "AI 포스트 생성" 클릭

### 3. 자동 포스팅
- "블로그에 자동 포스팅" 버튼 클릭
- 자동으로 네이버 블로그에 업로드됨

## 🎯 완전 자동화 플로우
1. 키워드 입력
2. AI가 포스트 생성 
3. 네이버에 자동 로그인
4. 생성된 포스트 자동 업로드
5. 완료!

## 💡 팁
- Chrome 설치가 가장 중요합니다
- 처음 실행 시 패키지 설치에 시간이 걸릴 수 있습니다
- Headless 모드로 실행되므로 브라우저 창이 보이지 않습니다
- 네이버 로그인 시 보안 문자가 있을 수 있습니다 (자동 처리)

Replit에서 완전한 네이버 블로그 자동화를 경험하세요! 🚀