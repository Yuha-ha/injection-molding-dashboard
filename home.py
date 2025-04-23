import streamlit as st
st.set_page_config(page_title="650톤 우진2호기", layout="wide")

from PIL import Image
import base64

# 각 페이지 모듈 import
import cn7
import rg3
import guide
import total

# ✅ 사이드바 숨기기
st.markdown("""
    <style>
    [data-testid="stSidebar"], [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
""", unsafe_allow_html=True)

# ✅ 배경 이미지 설정 함수
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
    """, unsafe_allow_html=True)

# ✅ 흰 배경으로 초기화하는 함수 (홈이 아닌 경우)
def clear_background():
    st.markdown("""
        <style>
        html, body, .stApp {
            background-image: none !important;
            background-color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ✅ 세션 상태 기반 페이지 이동
if "page" not in st.session_state:
    st.session_state.page = "home"

def go_to(page_name):
    st.session_state.page = page_name

import base64

def show_logo_top_left(image_path="images/woojin_logo.png"):
    with open(image_path, "rb") as img_file:
        logo_base64 = base64.b64encode(img_file.read()).decode()

    st.markdown(f"""
        <div style="position: absolute; top: 25px; left: 25px; z-index: 9999;">
            <img src="data:image/png;base64,{logo_base64}" style="height: 90px;">
        </div>
    """, unsafe_allow_html=True)

def render_home():
    set_background("images/background.png")
    show_logo_top_left()
    
    set_background("images/background.png")

    # ✅ 제목
    st.markdown("""
        <h1 style='text-align: center; color: white; font-size: 48px; font-weight: bold; line-height: 1.4;'>
            650톤-우진2호기<br>
            <span style='display: inline-block; padding-left: 30px;'>(DL650A5)</span>
        </h1>
    """, unsafe_allow_html=True)

    # ✅ 버튼 스타일
    st.markdown("""
        <style>
        /* 버튼 스타일만 적용 (간격 제외) */
        button[kind="secondary"] {
            font-size: 35px !important;
            font-weight: bold !important;
            padding: 24px 20px !important;
            width: 340px !important;
            height: 90px !important;
            border-radius: 14px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # ✅ 첫 번째 줄
    spacer1, col1, spacer_between, col2, spacer2 = st.columns([1.9, 2, 1.0, 2, 2.1])
    with col1:
        if st.button("📸 호기 종합 현황"):
            st.session_state.page = "total"
    with col2:
        if st.button("🚗 아반떼 (cn7)"):
            st.session_state.page = "cn7"

    st.markdown("<div style='height: 40px;'></div>", unsafe_allow_html=True)  # 상하 간격

    # ✅ 두 번째 줄
    spacer3, col3, spacer_between2, col4, spacer4 = st.columns([1.9, 2, 1.0, 2, 2.1])
    with col3:
        if st.button("📖 불량 가이드북"):
            st.session_state.page = "guide"
    with col4:
        if st.button("🚙 제네시스 G80 (rg3)"):
            st.session_state.page = "rg3"


# ✅ 페이지 라우팅
if st.session_state.page == "home":
    render_home()
else:
    clear_background()  # ✅ 홈이 아니면 배경 제거
    if st.session_state.page == "guide":
        guide.render()
    elif st.session_state.page == "cn7":
        cn7.render()
    elif st.session_state.page == "rg3":
        rg3.render()
    elif st.session_state.page == "total":
        total.render()