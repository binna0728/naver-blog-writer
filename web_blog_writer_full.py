"""
🌐 네이버 블로그 자동 작성기 - Replit 완전 자동화 버전
- AI 포스트 생성 + 자동 로그인 + 자동 포스팅
- Replit 환경에서 Selenium 완벽 지원
"""

import streamlit as st
import threading
import time
import json
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from geminiapi import GeminiAPI
import pandas as pd

class FullBlogWriter:
    def __init__(self):
        self.driver = None
        self.gemini_api = None
        
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if 'naver_id' not in st.session_state:
            st.session_state.naver_id = ""
        if 'naver_pw' not in st.session_state:
            st.session_state.naver_pw = ""
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
        if 'login_status' not in st.session_state:
            st.session_state.login_status = False
        if 'generated_posts' not in st.session_state:
            st.session_state.generated_posts = []
        if 'is_running' not in st.session_state:
            st.session_state.is_running = False

    def setup_driver(self):
        """Replit용 Chrome 드라이버 설정"""
        try:
            options = Options()
            
            # Replit 환경 최적화 설정
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-plugins")
            options.add_argument("--disable-images")
            options.add_argument("--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")
            
            # Chrome 바이너리 경로 (Replit 환경)
            options.binary_location = "/nix/store/4jk6b9z2ka2dz0p6w4y4k8cfjw80z3l5-chromium-120.0.6099.109/bin/chromium"
            
            try:
                # ChromeDriverManager 사용
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            except Exception:
                # 대안: 시스템 크롬 드라이버
                self.driver = webdriver.Chrome(options=options)
            
            return True
        except Exception as e:
            st.error(f"드라이버 설정 실패: {str(e)}")
            return False

    def test_login(self, naver_id, naver_pw):
        """네이버 로그인 테스트"""
        try:
            if not self.setup_driver():
                return False
                
            self.driver.get("https://nid.naver.com/nidlogin.login")
            
            # 아이디 입력
            id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "id"))
            )
            id_input.clear()
            id_input.send_keys(naver_id)
            
            # 비밀번호 입력
            pw_input = self.driver.find_element(By.ID, "pw")
            pw_input.clear()
            pw_input.send_keys(naver_pw)
            
            # 로그인 버튼 클릭
            login_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "log.login"))
            )
            login_btn.click()
            
            time.sleep(3)
            current_url = self.driver.current_url
            
            success = ("naver.com" in current_url and "login" not in current_url)
            
            if self.driver:
                self.driver.quit()
                
            return success
                
        except Exception as e:
            st.error(f"로그인 테스트 실패: {str(e)}")
            if self.driver:
                self.driver.quit()
            return False

    def generate_posts_with_ai(self, keyword, count, api_key, writing_style="일반적인"):
        """AI를 사용하여 포스트 생성"""
        try:
            gemini_api = GeminiAPI(api_key)
            posts = []
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(count):
                status_text.text(f"포스트 {i+1}/{count} 생성 중...")
                progress_bar.progress((i + 1) / count)
                
                # 제목 생성
                title_prompt = f"'{keyword}' 관련 블로그 포스트 제목을 1개만 생성해주세요. 흥미롭고 클릭하고 싶은 제목으로 만들어주세요."
                title = gemini_api.generate_content(title_prompt).strip()
                
                # 내용 생성
                content_prompt = f"""
                '{title}' 제목으로 {writing_style} 스타일의 블로그 포스트를 작성해주세요.
                
                2000자 이상으로 다음 구조로 작성:
                1. 도입부: 독자의 관심을 끄는 시작
                2. 본문: '{keyword}'에 대한 상세하고 유익한 정보  
                3. 실용적인 팁이나 방법 제시
                4. 마무리: 독자에게 도움이 되는 조언
                
                SEO를 고려하여 '{keyword}' 키워드를 자연스럽게 포함해주세요.
                """
                
                content = gemini_api.generate_content(content_prompt)
                
                posts.append({
                    'title': title,
                    'content': content,
                    'keyword': keyword,
                    'style': writing_style,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'word_count': len(content)
                })
                
                time.sleep(1)
            
            status_text.text("포스트 생성 완료! ✨")
            progress_bar.progress(1.0)
            return posts
            
        except Exception as e:
            st.error(f"포스트 생성 실패: {str(e)}")
            return []

    def auto_post_to_blog(self, posts, naver_id, naver_pw):
        """자동으로 블로그에 포스팅"""
        try:
            if not self.setup_driver():
                return False
            
            # 네이버 로그인
            self.driver.get("https://nid.naver.com/nidlogin.login")
            
            id_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "id"))
            )
            id_input.clear()
            id_input.send_keys(naver_id)
            
            pw_input = self.driver.find_element(By.ID, "pw")
            pw_input.clear()
            pw_input.send_keys(naver_pw)
            
            login_btn = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.ID, "log.login"))
            )
            login_btn.click()
            
            time.sleep(3)
            
            # 블로그 작성 페이지로 이동
            self.driver.get("https://blog.naver.com/PostWriteForm.naver")
            time.sleep(5)
            
            success_count = 0
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, post in enumerate(posts):
                try:
                    status_text.text(f"포스팅 {i+1}/{len(posts)}: {post['title'][:30]}...")
                    progress_bar.progress((i + 1) / len(posts))
                    
                    # 제목 입력
                    title_input = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "input.se-input"))
                    )
                    title_input.clear()
                    title_input.send_keys(post['title'])
                    
                    # 내용 입력 (iframe 처리)
                    iframe = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "iframe.se-module-text"))
                    )
                    self.driver.switch_to.frame(iframe)
                    
                    content_area = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.TAG_NAME, "body"))
                    )
                    content_area.clear()
                    content_area.send_keys(post['content'])
                    
                    self.driver.switch_to.default_content()
                    
                    # 발행 버튼 클릭
                    publish_btn = WebDriverWait(self.driver, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.publish"))
                    )
                    publish_btn.click()
                    
                    time.sleep(3)
                    success_count += 1
                    
                    # 다음 포스트를 위해 새 작성 페이지로 이동
                    if i < len(posts) - 1:
                        self.driver.get("https://blog.naver.com/PostWriteForm.naver")
                        time.sleep(5)
                        
                except Exception as e:
                    st.error(f"포스트 '{post['title']}' 업로드 실패: {str(e)}")
                    continue
            
            status_text.text(f"자동 포스팅 완료! 성공: {success_count}/{len(posts)}")
            return success_count > 0
            
        except Exception as e:
            st.error(f"자동 포스팅 실패: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

def main():
    st.set_page_config(
        page_title="네이버 블로그 완전 자동화",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 다크 테마 CSS
    st.markdown("""
    <style>
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🚀 네이버 블로그 완전 자동화")
    st.success("✅ **Replit 전용** - 자동 로그인 + 자동 포스팅 지원")
    st.info("🤖 AI 포스트 생성부터 블로그 업로드까지 완전 자동화!")
    
    st.markdown("---")
    
    writer = FullBlogWriter()
    writer.initialize_session_state()
    
    # 사이드바 - 로그인 정보
    with st.sidebar:
        st.header("🔐 네이버 계정")
        
        naver_id = st.text_input("네이버 아이디", value=st.session_state.naver_id)
        naver_pw = st.text_input("네이버 비밀번호", type="password", value=st.session_state.naver_pw)
        
        if st.button("🔍 로그인 테스트"):
            if naver_id and naver_pw:
                with st.spinner("로그인 테스트 중..."):
                    if writer.test_login(naver_id, naver_pw):
                        st.success("✅ 로그인 성공!")
                        st.session_state.login_status = True
                        st.session_state.naver_id = naver_id
                        st.session_state.naver_pw = naver_pw
                    else:
                        st.error("❌ 로그인 실패!")
            else:
                st.error("아이디와 비밀번호를 입력하세요")
        
        st.markdown("---")
        
        st.header("🤖 AI 설정")
        api_key = st.text_input("Google AI API 키", type="password", value=st.session_state.api_key)
        
        if st.button("🧪 API 테스트"):
            if api_key:
                try:
                    gemini_api = GeminiAPI(api_key)
                    test_response = gemini_api.generate_content("테스트")
                    if test_response:
                        st.success("✅ API 연결 성공!")
                        st.session_state.api_key = api_key
                    else:
                        st.error("❌ API 연결 실패!")
                except Exception as e:
                    st.error(f"❌ API 오류: {str(e)}")
            else:
                st.error("API 키를 입력하세요")
    
    # 메인 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 포스트 생성 설정")
        
        keyword = st.text_input("키워드", placeholder="예: 맛집, 여행, 건강, 요리")
        
        col_count, col_style = st.columns([1, 1])
        with col_count:
            post_count = st.number_input("포스트 수", min_value=1, max_value=10, value=3)
        with col_style:
            writing_style = st.selectbox("글쓰기 스타일", 
                ["일반적인", "친근한", "전문적인", "유머러스한"])
        
        if st.button("🤖 AI 포스트 생성"):
            if not keyword:
                st.error("키워드를 입력하세요")
            elif not api_key:
                st.error("API 키를 입력하세요")
            else:
                with st.spinner("AI가 포스트 생성 중..."):
                    posts = writer.generate_posts_with_ai(keyword, post_count, api_key, writing_style)
                    if posts:
                        st.session_state.generated_posts = posts
                        st.success(f"✅ {len(posts)}개 포스트 생성 완료!")
    
    with col2:
        st.header("🚀 자동 포스팅")
        
        if st.session_state.generated_posts:
            st.success(f"📝 {len(st.session_state.generated_posts)}개 포스트 준비됨")
            
            if st.button("📤 블로그에 자동 포스팅", disabled=st.session_state.is_running):
                if not st.session_state.naver_id or not st.session_state.naver_pw:
                    st.error("네이버 계정 정보를 입력하고 테스트하세요")
                else:
                    st.session_state.is_running = True
                    with st.spinner("자동 포스팅 진행 중..."):
                        success = writer.auto_post_to_blog(
                            st.session_state.generated_posts,
                            st.session_state.naver_id,
                            st.session_state.naver_pw
                        )
                        if success:
                            st.success("🎉 자동 포스팅 완료!")
                            st.balloons()
                        else:
                            st.error("❌ 포스팅 중 오류 발생")
                    st.session_state.is_running = False
        else:
            st.info("먼저 포스트를 생성하세요")
    
    # 생성된 포스트 미리보기
    if st.session_state.generated_posts:
        st.header("📋 생성된 포스트")
        
        for i, post in enumerate(st.session_state.generated_posts[-3:]):  # 최근 3개만 표시
            with st.expander(f"📄 {post['title']}", expanded=False):
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.write(f"**키워드**: {post['keyword']}")
                    st.write(f"**스타일**: {post['style']}")
                with col_info2:
                    st.write(f"**글자수**: {post['word_count']:,}자")
                    st.write(f"**생성일**: {post['created_at']}")
                
                st.text_area("내용 미리보기", value=post['content'][:500] + "...", height=150, key=f"preview_{i}")

if __name__ == "__main__":
    main()