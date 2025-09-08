"""
🌐 네이버 블로그 자동 작성기 - 간소화 버전
- AI 포스트 생성 기능만 포함
- Streamlit Cloud 배포 최적화
"""

import streamlit as st
import time
import json
from datetime import datetime
from geminiapi import GeminiAPI
import pandas as pd

class SimpleBlogWriter:
    def __init__(self):
        self.gemini_api = None
        
    def initialize_session_state(self):
        """세션 상태 초기화"""
        if 'api_key' not in st.session_state:
            st.session_state.api_key = ""
        if 'generated_posts' not in st.session_state:
            st.session_state.generated_posts = []
        if 'is_generating' not in st.session_state:
            st.session_state.is_generating = False

    def test_api_connection(self, api_key):
        """API 연결 테스트"""
        try:
            gemini_api = GeminiAPI(api_key)
            test_response = gemini_api.generate_content("테스트")
            return bool(test_response and len(test_response.strip()) > 0)
        except Exception as e:
            st.error(f"API 테스트 실패: {str(e)}")
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
                
                # 다양한 제목 스타일
                title_styles = [
                    f"'{keyword}' 완벽 가이드",
                    f"{keyword} 추천 BEST 5",
                    f"{keyword}에 대한 모든 것",
                    f"{keyword} 초보자도 쉽게!",
                    f"2024년 {keyword} 트렌드",
                    f"{keyword} 후기와 경험담",
                    f"{keyword} 비교 분석",
                    f"{keyword}로 시작하는 새로운 경험"
                ]
                
                # 제목 생성
                if i < len(title_styles):
                    title = title_styles[i]
                else:
                    title_prompt = f"'{keyword}' 관련 블로그 포스트 제목을 1개만 생성해주세요. 흥미롭고 클릭하고 싶은 제목으로 만들어주세요."
                    title = gemini_api.generate_content(title_prompt).strip()
                
                # 글쓰기 스타일에 따른 프롬프트 조정
                if writing_style == "전문적인":
                    style_instruction = "전문적이고 신뢰할 수 있는 톤으로, 구체적인 데이터와 근거를 포함하여"
                elif writing_style == "친근한":
                    style_instruction = "친근하고 편안한 말투로, 개인적인 경험담을 포함하여"
                elif writing_style == "유머러스한":
                    style_instruction = "재미있고 유머러스한 톤으로, 독자의 웃음을 유발할 수 있도록"
                else:
                    style_instruction = "자연스럽고 읽기 쉬운 톤으로"
                
                # 내용 생성
                content_prompt = f"""
                '{title}' 제목으로 블로그 포스트를 {style_instruction} 작성해주세요.
                
                다음 구조로 2000자 이상 작성해주세요:
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
                
                time.sleep(1)  # API 요청 간격
            
            status_text.text("포스트 생성 완료! ✨")
            progress_bar.progress(1.0)
            return posts
            
        except Exception as e:
            st.error(f"포스트 생성 실패: {str(e)}")
            return []

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
    .success-box {
        background-color: #1f2937;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #10b981;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.title("🚀 AI 블로그 포스트 생성기")
    
    # 간소화 버전 알림
    st.info("📱 **간소화 버전** - AI 포스트 생성 기능에 특화된 웹 앱입니다")
    st.success("✅ **장점**: 빠른 로딩, 안정적인 실행, 모바일 최적화")
    
    st.markdown("---")
    
    writer = SimpleBlogWriter()
    writer.initialize_session_state()
    
    # 사이드바 - API 설정
    with st.sidebar:
        st.header("🔧 API 설정")
        
        api_key = st.text_input(
            "Google AI API 키", 
            type="password", 
            value=st.session_state.api_key,
            help="Google AI Studio에서 발급받은 API 키를 입력하세요"
        )
        
        if st.button("🧪 API 연결 테스트"):
            if api_key:
                with st.spinner("API 연결 테스트 중..."):
                    if writer.test_api_connection(api_key):
                        st.success("✅ API 연결 성공!")
                        st.session_state.api_key = api_key
                    else:
                        st.error("❌ API 연결 실패!")
            else:
                st.error("API 키를 입력해주세요.")
        
        st.markdown("---")
        
        st.header("📊 생성 통계")
        if st.session_state.generated_posts:
            total_posts = len(st.session_state.generated_posts)
            total_words = sum(post.get('word_count', 0) for post in st.session_state.generated_posts)
            st.metric("생성된 포스트", total_posts)
            st.metric("총 글자 수", f"{total_words:,}")
        else:
            st.info("아직 생성된 포스트가 없습니다.")
    
    # 메인 영역
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("✍️ 포스트 생성")
        
        keyword = st.text_input(
            "키워드", 
            placeholder="예: 맛집, 여행, 요리, 건강",
            help="포스트 주제가 될 키워드를 입력하세요"
        )
        
        col_count, col_style = st.columns([1, 1])
        
        with col_count:
            post_count = st.number_input("생성할 포스트 수", min_value=1, max_value=10, value=3)
        
        with col_style:
            writing_style = st.selectbox(
                "글쓰기 스타일",
                ["일반적인", "친근한", "전문적인", "유머러스한"]
            )
        
        if st.button("🤖 AI 포스트 생성", disabled=st.session_state.is_generating):
            if not keyword:
                st.error("키워드를 입력해주세요.")
            elif not api_key:
                st.error("API 키를 입력해주세요.")
            else:
                st.session_state.is_generating = True
                with st.spinner("AI가 포스트를 생성하고 있습니다..."):
                    posts = writer.generate_posts_with_ai(keyword, post_count, api_key, writing_style)
                    if posts:
                        st.session_state.generated_posts.extend(posts)
                        st.success(f"✅ {len(posts)}개 포스트 생성 완료!")
                        st.balloons()
                st.session_state.is_generating = False
    
    with col2:
        st.header("📤 포스트 활용")
        
        if st.session_state.generated_posts:
            st.success(f"💡 총 {len(st.session_state.generated_posts)}개 포스트가 생성되었습니다!")
            
            # 최신 포스트 미리보기
            latest_post = st.session_state.generated_posts[-1]
            st.write("**최신 생성 포스트:**")
            st.write(f"📝 {latest_post['title']}")
            st.write(f"🔤 {latest_post['word_count']:,}자")
            
            # 다운로드 옵션
            st.subheader("📥 다운로드")
            
            # CSV 다운로드
            df = pd.DataFrame(st.session_state.generated_posts)
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📄 CSV 파일 다운로드",
                data=csv,
                file_name=f"blog_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help="엑셀에서 열 수 있는 CSV 파일로 다운로드"
            )
            
            # JSON 다운로드
            json_data = json.dumps(st.session_state.generated_posts, ensure_ascii=False, indent=2)
            st.download_button(
                label="📋 JSON 파일 다운로드",
                data=json_data,
                file_name=f"blog_posts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                help="프로그래밍에서 사용하기 쉬운 JSON 형식"
            )
            
            # 초기화 버튼
            if st.button("🗑️ 생성된 포스트 초기화"):
                st.session_state.generated_posts = []
                st.success("포스트가 초기화되었습니다.")
                st.experimental_rerun()
                
        else:
            st.info("포스트를 생성하면 여기에서 다운로드할 수 있습니다.")
    
    # 생성된 포스트 목록
    if st.session_state.generated_posts:
        st.header("📚 생성된 포스트 미리보기")
        
        # 탭으로 구분
        tabs = st.tabs([f"포스트 {i+1}" for i in range(min(5, len(st.session_state.generated_posts)))])
        
        for i, tab in enumerate(tabs):
            if i < len(st.session_state.generated_posts):
                post = st.session_state.generated_posts[-(i+1)]  # 최신순 정렬
                with tab:
                    st.subheader(post['title'])
                    
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.write(f"**키워드:** {post['keyword']}")
                    with col_info2:
                        st.write(f"**스타일:** {post['style']}")
                    with col_info3:
                        st.write(f"**글자수:** {post['word_count']:,}자")
                    
                    st.write(f"**생성일:** {post['created_at']}")
                    
                    with st.expander("📖 포스트 내용 보기"):
                        st.text_area("", value=post['content'], height=300, key=f"post_content_{i}")
                    
                    # 개별 복사 버튼
                    if st.button(f"📋 클립보드에 복사", key=f"copy_{i}"):
                        # JavaScript를 통한 클립보드 복사는 Streamlit에서 제한적이므로
                        # 사용자에게 수동 복사를 안내
                        st.info("위의 텍스트 영역에서 내용을 선택하여 복사해주세요 (Ctrl+A, Ctrl+C)")

if __name__ == "__main__":
    main()