def render() :
    import streamlit as st
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib
    import base64

    # 🔹 제목 위 오른쪽에 홈 버튼 (한 줄 유지)
    col1, col2 = st.columns([9, 1])
    with col1:
        st.empty()
    with col2:
        st.markdown("""
            <style>
            div.stButton > button {
                white-space: nowrap;  /* ✅ 한 줄로 표시 */
                width: 160px;          /* 필요시 조정 가능 */
                font-size: 16px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='text-align: right; padding-top: 10px;'>", unsafe_allow_html=True)
        if st.button("🏠 홈으로 돌아가기"):
            st.session_state.page = "home"
        st.markdown("</div>", unsafe_allow_html=True)

    # ✅ 한글 폰트 깨짐 방지
    matplotlib.rcParams['font.family'] = 'NanumGothic'
    matplotlib.rcParams['axes.unicode_minus'] = False

    # ✅ 스타일 정의
    st.markdown("""
        <style>
            .title-center {
                text-align: center;
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 30px;
            }
            .boxed {
                border: 1px solid #ccc;
                padding: 20px;
                border-radius: 10px;
                background-color: #f9f9f9;
            }
            .kpi {
                text-align: center;
                font-size: 28px;
                font-weight: bold;
            }
            .kpi-label {
                text-align: center;
                font-size: 16px;
                color: #555;
            }
        </style>
    """, unsafe_allow_html=True)

    # ✅ 이미지 인코딩 함수
    def get_base64_image(image_path):
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    # ✅ 로고 삽입
    logo_base64 = get_base64_image("images/woojin_logo.png")
    st.markdown(f"""
        <div style="display: flex; justify-content: flex-start; align-items: center;">
            <img src="data:image/png;base64,{logo_base64}" style="height: 60px;">
        </div>
    """, unsafe_allow_html=True)

    # ✅ 제목
    st.markdown('<div class="title-center">호기 종합 현황</div>', unsafe_allow_html=True)

    # ✅ 데이터 로드 및 날짜 필터링
    df = pd.read_csv("Merged_Defect_Data.csv", parse_dates=['TimeStamp'])
    df = df[(df['TimeStamp'] >= '2020-03-25') & (df['TimeStamp'] <= '2020-10-20')]

    # 전체 생산량(1.55%로 가정했을 시)
    total_product = 136971613

    # ✅ KPI 계산
    total_defect = int(df['ERR_FACT_QTY_TOTAL'].sum())
    defect_rate = round((total_defect / total_product) * 100, 2)
    latest_date = df['TimeStamp'].max().strftime('%Y-%m-%d')
    latest_7_avg = round(df.sort_values('TimeStamp').tail(7)['ERR_FACT_QTY_TOTAL'].mean(), 1)

    # ✅ KPI 박스 표시
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f'<div class="boxed"><div class="kpi">{defect_rate}%</div><div class="kpi-label">누적 불량률 (전체 생산량 대비)</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="boxed"><div class="kpi">{latest_7_avg}</div><div class="kpi-label">최근 7일 평균 불량</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="boxed"><div class="kpi">{latest_date}</div><div class="kpi-label">최근 불량 발생일</div></div>', unsafe_allow_html=True)

    st.markdown("---")

    # ✅ 이미지 + 사양 + 최대 불량일 표
    col4, col5 = st.columns([1.5, 1.5])

    with col4:
        st.markdown("""
            <div style="display: flex; align-items: center; gap: 20px;">
                <div style="flex: 1.5;">
                    <img src="data:image/png;base64,%s" style="width: 100%%; height: auto;">
                </div>
                <div style="flex: 1; display: flex; align-items: center; justify-content: center;">
                    <div style="text-align: left; font-size: 18px; line-height: 1.8;">
                        <p><strong>기종 :</strong> DL650A5</p>
                        <p><strong>사출기호 :</strong> IH5900</p>
                        <p><strong>스크류&바렐타입 :</strong> A형</p>
                        <p><strong>수지원료 :</strong> TPV</p>
                    </div>
                </div>
            </div>
        """ % get_base64_image("images/woojin_2ho.png"), unsafe_allow_html=True)

    with col5:
        # 하루 생산량 설정
        daily_production = 1426788

        # 불량률 컬럼 추가
        df["DefectRate"] = (df["ERR_FACT_QTY_TOTAL"] / daily_production) * 100

        # 불량률 기준 상위 3일 추출
        top3 = df.sort_values('DefectRate', ascending=False).head(3)

        st.markdown("""
            <div class="boxed">
                <div style="font-size:20px; font-weight:bold; text-align:center;">
                    최대 불량률 발생일
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div style="width: 100%; margin-top: 10px;">
                <table style="width: 100%; border-collapse: collapse; text-align: center; font-size: 16px;">
                    <thead>
                        <tr style="border-bottom: 1px solid #ccc;">
                            <th>날짜</th>
                            <th>불량률 (%)</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join([
                            f"<tr><td>{row['TimeStamp'].date()}</td><td>{row['DefectRate']:.2f}%</td></tr>"
                            for _, row in top3.iterrows()
                        ])}
                    </tbody>
                </table>
            </div>
        """, unsafe_allow_html=True)


    # ✅ 그래프 구역
    col6, col7 = st.columns(2)

    with col6:
        st.markdown("""
            <div class="boxed">
                <div style="font-size:20px; font-weight:bold; text-align:center;">
                    일별 불량 수
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 날짜 슬라이더 설정
        min_date = df['TimeStamp'].min().date()
        max_date = df['TimeStamp'].max().date()
        start_date, end_date = st.slider(
            "📅 일별 불량 데이터를 조회할 기간을 선택하세요",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="YYYY-MM-DD"
        )

        # 날짜 필터링
        mask = (df['TimeStamp'] >= pd.to_datetime(start_date)) & (df['TimeStamp'] <= pd.to_datetime(end_date))
        filtered_df = df[mask]

        # 간격 간단하게 보기 좋게
        tick_dates = pd.date_range(start=filtered_df['TimeStamp'].min(), end=filtered_df['TimeStamp'].max(), periods=8)

        # 그래프
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.bar(filtered_df['TimeStamp'], filtered_df['ERR_FACT_QTY_TOTAL'], color="#f9dc8c")
        ax.axhline(filtered_df['ERR_FACT_QTY_TOTAL'].mean(), color="gray", linestyle="--", label="평균선")
        ax.set_xticks(tick_dates)
        ax.set_xticklabels([d.strftime('%Y-%m-%d') for d in tick_dates], rotation=45)
        ax.legend()
        st.pyplot(fig)

    with col7:
        st.markdown("""
            <div class="boxed">
                <div style="font-size:20px; font-weight:bold; text-align:center;">
                    월별 불량 수
                </div>
            </div>
        """, unsafe_allow_html=True)

        df['YearMonth'] = df['TimeStamp'].dt.to_period('M').astype(str)
        monthly = df.groupby('YearMonth')['ERR_FACT_QTY_TOTAL'].sum().reset_index()

        fig2, ax2 = plt.subplots(figsize=(6, 3))
        ax2.bar(monthly['YearMonth'], monthly['ERR_FACT_QTY_TOTAL'], color="#b5ead7")
        ax2.tick_params(axis='x', rotation=45)
        st.pyplot(fig2)