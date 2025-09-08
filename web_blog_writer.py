"""
🌐 웹 기반 네이버 블로그 자동 작성기
- Streamlit을 사용한 웹 앱 버전
- 모바일 브라우저에서 실행 가능
"""

import streamlit as st
import threading
import time
import base64
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

class WebBlogWriter:
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
        """Chrome 드라이버 설정"""
        try:
            options = Options()
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
            
            # 모바일에서는 헤드리스 모드 사용
            if st.checkbox("헤드리스 모드 (백그라운드 실행)", value=True):
                options.add_argument("--headless")
            
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
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
            
            if ("naver.com" in current_url and "login" not in current_url):
                return True
            else:
                return False
                
        except Exception as e:
            st.error(f"로그인 테스트 실패: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

    def generate_posts_with_ai(self, keyword, count, api_key):
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
                content_prompt = f"'{title}' 제목으로 블로그 포스트를 작성해주세요. 2000자 이상으로 상세하고 유익한 내용으로 작성해주세요."
                content = gemini_api.generate_content(content_prompt)
                
                posts.append({
                    'title': title,
                    'content': content,
                    'keyword': keyword,
                    'created_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
                
                time.sleep(1)  # API 요청 간격
            
            status_text.text("포스트 생성 완료!")
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
            
            status_text.text(f"포스팅 완료! 성공: {success_count}/{len(posts)}")
            return success_count > 0
            
        except Exception as e:
            st.error(f"자동 포스팅 실패: {str(e)}")
            return False
        finally:
            if self.driver:
                self.driver.quit()

def main():
    st.set_page_config(
        page_title="네이버 블로그 자동 작성기",
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
    .st-emotion-cache-1d391kg {
        background-color: #1e293b;
    }
    .st-emotion-cache-16txtl3 {
        background-color: #334155;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🚀 네이버 블로그 자동 작성기")
    st.markdown("---")
    
    writer = WebBlogWriter()
    writer.initialize_session_state()
    
    # 사이드바 - 로그인 정보
    with st.sidebar:
        st.header("🔐 로그인 정보")
        
        naver_id = st.text_input("네이버 아이디", value=st.session_state.naver_id)
        naver_pw = st.text_input("네이버 비밀번호", type="password", value=st.session_state.naver_pw)
        api_key = st.text_input("Google API 키", type="password", value=st.session_state.api_key)
        
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
                        st.session_state.login_status = False
            else:
                st.error("아이디와 비밀번호를 입력해주세요.")
        
        if st.button("🧪 API 테스트"):
            if api_key:
                try:
                    gemini_api = GeminiAPI(api_key)
                    test_response = gemini_api.generate_content("안녕하세요")
                    if test_response:
                        st.success("✅ API 연결 성공!")
                        st.session_state.api_key = api_key
                    else:
                        st.error("❌ API 연결 실패!")
                except Exception as e:
                    st.error(f"❌ API 오류: {str(e)}")
            else:
                st.error("API 키를 입력해주세요.")
    
    # 메인 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📝 포스트 생성")
        
        keyword = st.text_input("키워드", placeholder="예: 맛집, 여행, 요리")
        post_count = st.number_input("생성할 포스트 수", min_value=1, max_value=20, value=5)
        
        if st.button("🤖 포스트 생성"):
            if keyword and api_key:
                with st.spinner("AI가 포스트를 생성하고 있습니다..."):
                    posts = writer.generate_posts_with_ai(keyword, post_count, api_key)
                    if posts:
                        st.session_state.generated_posts = posts
                        st.success(f"✅ {len(posts)}개 포스트 생성 완료!")
            else:
                st.error("키워드와 API 키를 입력해주세요.")
    
    with col2:
        st.header("🚀 자동 포스팅")
        
        if st.session_state.generated_posts:
            st.info(f"생성된 포스트: {len(st.session_state.generated_posts)}개")
            
            if st.button("📤 블로그에 자동 포스팅"):
                if st.session_state.naver_id and st.session_state.naver_pw:
                    with st.spinner("블로그에 포스팅하고 있습니다..."):
                        success = writer.auto_post_to_blog(
                            st.session_state.generated_posts,
                            st.session_state.naver_id,
                            st.session_state.naver_pw
                        )
                        if success:
                            st.success("✅ 자동 포스팅 완료!")
                        else:
                            st.error("❌ 포스팅 실패!")
                else:
                    st.error("네이버 로그인 정보를 입력하고 테스트해주세요.")
        else:
            st.info("먼저 포스트를 생성해주세요.")
    
    # 생성된 포스트 미리보기
    if st.session_state.generated_posts:
        st.header("📋 생성된 포스트 미리보기")
        
        for i, post in enumerate(st.session_state.generated_posts):
            with st.expander(f"{i+1}. {post['title']}", expanded=False):
                st.write(f"**키워드:** {post['keyword']}")
                st.write(f"**생성일:** {post['created_at']}")
                st.write("**내용:**")
                st.text_area("", value=post['content'], height=200, key=f"post_{i}")
        
        # 엑셀 다운로드
        if st.button("📥 엑셀로 다운로드"):
            df = pd.DataFrame(st.session_state.generated_posts)
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 CSV 파일 다운로드",
                data=csv,
                file_name=f"blog_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()