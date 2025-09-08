# 네이버 블로그 자동 포스팅 프로그램

## 설치 방법
1. Python 3.8+ 설치
2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

## 실행 방법
```bash
python naver_blog_poster.py
```

## 실행 파일 생성
```bash
pyinstaller --onefile --windowed --icon=icon.ico naver_blog_poster.py
```

## 기능
- GUI 인터페이스
- 네이버 자동 로그인
- 블로그 글 자동 작성
- 설정 저장/불러오기
- 템플릿 관리
- 예약 포스팅
- 진행상황 실시간 표시

## 주의사항
- 네이버 보안 정책에 따라 캡차나 추가 인증이 필요할 수 있습니다
- 과도한 사용은 계정 제재를 받을 수 있으니 적절히 사용하세요