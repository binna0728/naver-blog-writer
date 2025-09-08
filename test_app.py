import streamlit as st

st.set_page_config(
    page_title="네이버 블로그 자동 작성기",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 네이버 블로그 자동 작성기")
st.success("✅ Streamlit Cloud 배포 테스트 성공!")

st.info("📱 기본 버전이 정상 작동 중입니다.")

st.markdown("---")

st.header("📝 포스트 생성 (테스트)")

keyword = st.text_input("키워드", placeholder="예: 맛집, 여행")
count = st.number_input("포스트 수", min_value=1, max_value=5, value=1)

if st.button("🤖 테스트 생성"):
    if keyword:
        st.success(f"'{keyword}' 키워드로 {count}개 포스트를 생성했습니다! (시뮬레이션)")
        
        for i in range(count):
            with st.expander(f"포스트 {i+1}: {keyword} 관련 글"):
                st.write(f"**제목**: {keyword}에 대한 완벽 가이드 {i+1}")
                st.write(f"**내용**: {keyword}에 대한 자세한 설명과 유용한 정보를 제공하는 포스트입니다...")
    else:
        st.error("키워드를 입력해주세요.")