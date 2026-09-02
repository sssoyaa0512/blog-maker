import streamlit as st
import google.generativeai as genai

# 1. Gemini API 키 설정 (복사한 API 키로 변경하세요)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. 블로그 생성 함수 (Gemini API 사용 - 자동 모델 탐색 버전)
def generate_blog_post(topic, keywords, core_message):
    prompt = f"""
    당신은 10년 차 최고의 부동산 전문 블로거이자 친절한 멘토입니다. 
    사용자가 제공한 주제, 키워드, 핵심 문장을 바탕으로 네이버 블로그에 최적화된 글을 작성해주세요.
    단, 작성된 글을 보는 사람이 '왜 이 글이 잘 쓰여졌는지' 이해할 수 있도록, 
    각 단락(제목, 도입부, 본문, 마무리) 아래에 반드시 '>> 핵심 포인트: [이유]' 형식으로 설명을 덧붙여야 합니다.

    [작성 규칙 및 출력 예시]
    제목: (키워드를 조합한 직관적인 제목)
    >> 핵심 포인트: 검색 의도를 정확히 타겟팅한 직관적인 제목

    도입부: (공감대 형성과 3줄 요약)
    >> 핵심 포인트: 체류시간을 늘리는 도입부 (후킹과 요약)

    본문: (소제목 활용, 여백, 객관적 데이터와 인사이트 결합)
    >> 핵심 포인트: 모바일에 최적화된 시각적 구조와 객관적/주관적 데이터의 결합

    마무리: (내부 링크 유도 및 소통 유도 CTA)
    >> 핵심 포인트: 행동을 유도하는 깔끔한 마무리 (CTA)

    ---
    [사용자 입력 정보]
    주제: {topic}
    키워드: {keywords}
    전달할 핵심 내용: {core_message}
    
    위 사용자 입력 정보를 바탕으로 가이드에 맞춰 완벽한 블로그 글을 작성해줘.
    """

    try:
        # 에러 메시지의 권장 사항에 따라 최신 3.6 플래시 모델로 명시적 지정
        model = genai.GenerativeModel("gemini-3.6-flash")
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"오류가 발생했습니다: {e}"

# --- UI 화면 구성 (이전과 동일하게 유지) ---
st.set_page_config(page_title="부동산 블로그 자동 작성기", page_icon="🏡", layout="wide")

st.title("🏡 부동산 블로그 자동 작성기")
st.markdown("주제와 키워드만 입력하면 전문가 수준의 블로그 초안을 작성해 줍니다.")

# 가이드북 팝업
with st.expander("💡 [가이드북] 성공적인 부동산 블로그 핵심 특징 보기"):
    st.markdown("""
    **1. 검색 의도를 정확히 타겟팅한 직관적인 제목**
    인기 블로그는 사용자가 검색창에 입력할 만한 구체적인 키워드를 조합하여 제목을 짓습니다. 추상적이거나 감성적인 제목보다는 지역, 매물명, 목적이 명확히 드러나야 클릭률이 높습니다.
    * 나쁜 예: 살기 좋은 동네, 송파구 아파트 추천해요!
    * 좋은 예: [송파구] 헬리오시티 33평 임장 후기 및 최신 실거래가 시세 분석 

    **2. 체류시간을 늘리는 도입부 (후킹과 요약)**
    글을 클릭하고 첫 3초 안에 독자를 잡아두기 위해, 서론에서 이 글을 읽어야 하는 이유와 핵심을 먼저 짚어줍니다.
    * 공감대 형성: 최근 바뀐 부동산 정책, 금리 변동 등을 언급
    * 3줄 요약: 본문의 핵심(현재 시세, 추천 타겟 등)을 박스 형태로 요약

    **3. 모바일에 최적화된 시각적 구조와 가독성**
    독자의 70% 이상은 모바일로 읽습니다. 
    * 소제목 활용: 입지 및 교통, 학군 및 인프라 등으로 구분
    * 여백과 강조: 3~4줄마다 문단을 나누고 중요 정보는 강조

    **4. 객관적 데이터와 주관적 인사이트의 결합 (핵심)**
    데이터가 의미하는 바를 해석해 주는 글이 인게이지먼트를 폭발시킵니다.
    * 객관적 팩트: "최근 실거래가 14억 5천만 원입니다."
    * 전문가적 해석: "전세가율이 60%까지 올라왔고... 실거주 목적이라면 지금이 진입 적기입니다."

    **5. 행동을 유도하는 깔끔한 마무리 (CTA)**
    * 내부 링크 연결: "함께 읽으면 좋은 글" 링크 남기기
    * 소통 유도: "궁금한 점은 비밀댓글로 남겨주세요"
    """)

st.divider()

# 입력 폼
col1, col2 = st.columns(2)

with col1:
    topic = st.text_input("📝 블로그 주제 (예: 송파구 헬리오시티 임장 및 시세)", placeholder="주제를 입력하세요")
    keywords = st.text_input("🔑 핵심 키워드 (예: 송파구 아파트, 헬리오시티 시세, 33평)", placeholder="쉼표로 구분하여 입력하세요")
    core_message = st.text_area("🎯 꼭 전달하고 싶은 내용 (생각/인사이트)", 
                                placeholder="예: 주변에 학군이 좋아서 신혼부부나 어린 자녀를 둔 가족에게 추천하고 싶다. 현재 급매가 몇 개 있어서 지금 잡는 것이 이득이다.")
    
    submit_button = st.button("🚀 블로그 글 자동 생성하기")

# 결과 출력
with col2:
    st.subheader("결과물 확인 및 분석")
    if submit_button:
        if topic and keywords and core_message:
            with st.spinner("부동산 블로그 글을 작성 중입니다... ✍️"):
                result = generate_blog_post(topic, keywords, core_message)
                st.success("작성 완료!")
                st.markdown(result)
        else:
            st.warning("주제, 키워드, 핵심 내용을 모두 입력해주세요.")