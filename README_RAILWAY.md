# 🚄 Railway 배포 가이드

## 🚀 Railway로 배포하기

### 1단계: Railway 계정 생성
1. https://railway.app 접속
2. GitHub 계정으로 로그인

### 2단계: 프로젝트 배포
1. **"New Project"** 클릭
2. **"Deploy from GitHub repo"** 선택
3. **`binna0728/naver-blog-writer`** 선택
4. **"Deploy Now"** 클릭

### 3단계: 환경 설정 (자동)
Railway가 자동으로 감지:
- ✅ `requirements.txt` - Python 의존성
- ✅ `Procfile` - 시작 명령어
- ✅ `runtime.txt` - Python 버전
- ✅ `railway.json` - 배포 설정

### 4단계: 배포 완료
- Railway가 자동으로 빌드하고 배포
- 고유한 URL 생성 (예: `https://your-app.railway.app`)

## 🔧 주요 설정 파일들

### `Procfile`
```
web: streamlit run web_blog_writer_simple.py --server.port $PORT --server.address 0.0.0.0 --server.headless true
```

### `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "streamlit run web_blog_writer_simple.py --server.port $PORT --server.address 0.0.0.0 --server.headless true"
  }
}
```

## 🌟 Railway의 장점
- ✅ **GitHub 연동**: 코드 푸시 시 자동 배포
- ✅ **무료 플랜**: 월 500시간 무료
- ✅ **안정적**: Streamlit Cloud보다 안정적
- ✅ **빠른 배포**: 몇 분 내 배포 완료
- ✅ **SSL/HTTPS**: 자동 적용
- ✅ **커스텀 도메인**: 설정 가능

## 📱 배포 후 사용법
1. Railway에서 생성된 URL 접속
2. 모바일 브라우저에서도 접속 가능
3. Google AI API 키 입력하여 사용

## 🛠️ 문제 해결
- **빌드 실패**: Railway 대시보드에서 로그 확인
- **포트 문제**: `$PORT` 환경변수 자동 설정됨
- **의존성 문제**: `requirements.txt` 확인

Railway는 Streamlit Cloud보다 훨씬 안정적입니다! 🚀