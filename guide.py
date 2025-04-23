import streamlit as st
import base64

# ❗ 오류 방지를 위해 set_page_config는 main에서만 설정해야 하므로 여기에선 제거
def render() :    
    st.markdown("""
    <style>
        .block-container {
            max-width: 1000px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)

    # 🔹 제목 위 오른쪽에 홈 버튼 (한 줄 유지)
    col1, col2 = st.columns([9, 1])
    with col1:
        st.empty()
    with col2:
        st.markdown("""
            <style>
            div.stButton > button {
                white-space: nowrap;
                width: 160px;
                font-size: 16px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<div style='text-align: right; padding-top: 10px;'>", unsafe_allow_html=True)
        if st.button("🏠 홈으로 돌아가기"):
            st.session_state.page = "home"
        st.markdown("</div>", unsafe_allow_html=True)

    # 🔹 제목 (중앙 정렬 유지)
    st.markdown("""
        <h1 style='text-align: center; color: #2c3e50; font-size: 36px; font-weight: 700; padding-bottom: 20px;'>
            📘 불량 가이드북
        </h1>
    """, unsafe_allow_html=True)

    # 🔹 드롭다운 항목 구성
    options = {
        "초기허용불량": [],
        "가스": ["기포", "은조흔", "광택불량"],
        "미성형": ["쇼트숏", "플로우마크", "싱크마크"]
    }

    flat_options = []
    for group, items in options.items():
        flat_options.append(f"🔸 {group}")
        flat_options.extend(items)

    selected = st.selectbox("🔍 불량명을 선택하세요", ["선택하세요"] + flat_options)

    # ✅ 이미지 인코딩 함수
    def encode_image_to_base64(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    # ✅ 공통 스타일 정의
    st.markdown("""
    <style>
    .info-box {
        background-color: #fefefe;
        border: 1px solid #ccc;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
        line-height: 1.6;
        font-size: 15px;
    }
    .info-box b {
        color: #2c3e50;
    }
    .info-box ul {
        margin-top: 5px;
        padding-left: 18px;
    }
    .section-title {
        font-size: 20px;
        font-weight: bold;
        margin-top: 30px;
        color: #2c3e50;
    }
    .content-box {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dcdcdc;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ✅ 불량 항목 정보
    defect_data = {
        "초기허용불량": {
            "custom_html": [
                '<div class="section-title">🔹 1. 정의 / 설명</div>',
                """
                <div class="content-box">
                초기허용불량은 생산 시작 직후, 사출 공정이 완전히 안정되기 전에 발생할 수 있는 불량을 의미<br><br>
                이러한 불량은 온도, 압력, 속도 등의 조건이 기준치에 도달하지 않은 상태에서 나타나며,<br>
                일반적으로 일정 수량(예: 5~10개)은 허용 범위 내 불량으로 간주됨
                </div>""",
                '<div class="section-title">🔹 2. 발생 원인</div>',
                """
                <div class="content-box">
                ✅ 금형, 실린더 등의 예열 부족<br>
                ✅ 보압, 사출속도 등의 초기 조건 미세 불안정<br>
                ✅ 재료의 건조 부족<br>
                ✅ 센서나 장비의 초기 반응 지연</div>
                """,
                '<div class="section-title">🔹 3. 관리 방법 / 예방 조치</div>',
                """
                <div class="content-box">
                🛠️ 사출기, 금형 등 설비 예열 시간 확보<br>
                🧪 생산 전 더미 샷(Dummy shot) 실행<br>
                📋 조건 최적화된 레시피 호출<br>
                🌡️ 원재료의 건조 상태 점검<br>
                </div>"""
            ]
        },
        "기포": {
            "image": "images/기포.png",
            "category": "가스",
            "description": "성형품 내부에 공동을 일으키는 현상",
            "causes": "금형 내 압력 부족 또는 노즐 가스 방출 시 발생",
            "solutions": ["보압/사출압력 재조정", "가스 배출 설계 개선", "재료 건조 상태 점검 및 관리"]
        },
        "은조흔": {
            "image": "images/은조흔.png",
            "category": "가스",
            "description": "원료 흐름 방향을 따라 은백색 조흔이 나타나는 현상",
            "causes": "수분,가스가 고온·고속 사출 중 표면에 줄무늬를 형성하면서 발생",
            "solutions": ["사출 압력 및 속도 조정", "원재료 건조 철저히 관리", "금형 내 가스 배출 경로 확보"]
        },
        "광택불량": {
            "image": "images/광택불량.png",
            "category": "가스",
            "description": "표면 광택 저하 또는 투명 제품의 흐림 현상이 발생하는 불량",
            "causes": "플라스틱의 압착 부족이나 가스 응축으로 접착이 불량해져 발생함",
            "solutions": ["금형 예열 온도 점검 및 유지", "이형제 사용 최소화", "수지 가열 및 건조 조건 최적화"]
        },
        "쇼트숏": {
            "image": "images/쇼트숏.png",
            "category": "미성형",
            "description": "금형 내에서 원료 플라스틱의 충전량이 부족해서 나타남",
            "causes": "원료 공급 불량, 압력 부족, 유동 중 고화, 공기 저항으로 발생",
            "solutions": ["사출 속도 조정으로 흐름 안정화", "금형 및 수지 온도 상승", "게이트/러너 설계 최적화"]
        },
        "플로우마크": {
            "image": "images/플로우마크.png",
            "category": "미성형",
            "description": "금형 내 수지 흐름으로 생기는 줄무늬 형태의 결함",
            "causes": "게이트 설계 불량, 유속 변화, 냉각 불균형 등이 원인",
            "solutions": ["사출 속도 조정으로 흐름 안정화", "수지/금형 온도 균일화", "유동 방향 고려한 게이트 위치 조정"]
        },
        "싱크마크": {
            "image": "images/싱크마크.png",
            "category": "미성형",
            "description": "성형품 표면에 발생하는 함몰현상",
            "causes": "냉각 수축과 압력 저하에 따른 팽창 간 균형 붕괴가 원인",
            "solutions": ["보압 시간 및 압력 증가", "냉각 시간 조절", "제품 두께 및 리브 설계 최적화"]
        }
    }

    # ✅ 선택값 출력
    if selected.startswith("🔸 "):
        group = selected.replace("🔸 ", "")
        if group == "초기허용불량":
            data = defect_data[group]
            for html in data["custom_html"]:
                st.markdown(html, unsafe_allow_html=True)
        else:
            for item in options.get(group, []):
                data = defect_data[item]
                encoded_img = encode_image_to_base64(data["image"])
                st.markdown(f'<div class="section-title">🔹 현상 이름: {item}</div>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="display: flex; align-items: stretch; gap: 16px;">
                    <div style="flex-shrink: 0;">
                        <img src="data:image/png;base64,{encoded_img}" 
                            style="height: 100%; width: 240px; object-fit: cover; border-radius: 8px;" />
                    </div>
                    <div style="flex: 1;">
                        <div class="info-box" style="padding: 14px; height: 100%;">
                            <b>분류:</b> {data["category"]}<br><br>
                            <b>설명:</b><br>
                            {data["description"]}<br>
                            {data["causes"]}<br><br>
                            <b>해결 방안:</b>
                            <ul>
                                {''.join(f"<li>{item}</li>" for item in data["solutions"])}
                            </ul>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    elif selected in defect_data:
        data = defect_data[selected]
        if "custom_html" in data:
            for html in data["custom_html"]:
                st.markdown(html, unsafe_allow_html=True)
        else:
            encoded_img = encode_image_to_base64(data["image"])
            st.markdown(f'<div class="section-title">🔹 현상 이름: {selected}</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div style="display: flex; align-items: stretch; gap: 16px;">
                <div style="flex-shrink: 0;">
                    <img src="data:image/png;base64,{encoded_img}" 
                        style="height: 100%; width: 240px; object-fit: cover; border-radius: 8px;" />
                </div>
                <div style="flex: 1;">
                    <div class="info-box" style="padding: 14px; height: 100%;">
                        <b>분류:</b> {data["category"]}<br><br>
                        <b>설명:</b><br>
                        {data["description"]}<br>
                        {data["causes"]}<br><br>
                        <b>해결 방안:</b>
                        <ul>
                            {''.join(f"<li>{item}</li>" for item in data["solutions"])}
                        </ul>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
