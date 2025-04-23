def render() :
    import streamlit as st
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import plotly.graph_objects as go
    from sklearn.metrics.pairwise import euclidean_distances
    import matplotlib
    import matplotlib.font_manager as fm

    font_path = "fonts/NanumGothicCoding.ttf"  # 상대 경로
    font_prop = fm.FontProperties(fname=font_path, size=16, weight='bold')
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

    # 모델 & 데이터 로드
    with open('cn7_xgb_model.pkl', 'rb') as f:
        cn7_model = pickle.load(f)

    labeled_data = pd.read_csv('labeled_cn7.csv')
    data = pd.read_csv('cn7_augmented_defective_data.csv')

    # 파생 변수
    def calculate_derived_features(max_injection_speed, hopper_temp, barrel_temp_1):
        screw_area = 63.62
        injection_rate = screw_area * (max_injection_speed / 10)
        avg_material_temp = (hopper_temp + barrel_temp_1) / 2
        return injection_rate, avg_material_temp

    feature_means = {
        'Injection_Time': 9.58,
        'Plasticizing_Time': 16.82,
        'Cycle_Time': 59.55,
        'Average_Screw_RPM': 119.14,
        'Max_Switch_Over_Pressure': 119.33,
        'Average_Back_Pressure': 13.93,
        'Mold_Temperature_4': 43.58,
        'Max_Injection_Speed': 168.75,
        'Hopper_Temperature': 61.17,
        'Barrel_Temperature_1': 243.64
    }

    reason_images = {
        '초기허용불량': 'reason1.png',
        '가스': 'reason2.png',
        '미성형': 'reason3.png'
    }

    col1, col2 = st.columns([7, 1])  # 비율은 조정 가능

    with col1:
        st.markdown("<h1 style='text-align: left;'>Avante (CN7) 불량 예측 대시보드</h1>", unsafe_allow_html=True)

    with col2:
        # ✅ 버튼 스타일 먼저 삽입 (한 줄 유지 + 너비 강제)
        st.markdown("""
            <style>
            div.stButton > button {
                width: 160px;
                white-space: nowrap;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<div style='text-align: right; padding-top: 15px;'>", unsafe_allow_html=True)
        if st.button("🏠 홈으로 돌아가기"):
            st.session_state.page = "home"
        st.markdown("</div>", unsafe_allow_html=True)

    main_col1, main_col2 = st.columns([1, 3])

    # 수치 입력
    with main_col1:
        predict_button = st.button("불량 예측 실행")
        
        st.markdown("<h3 style='font-size:20px;'>수치 입력</h3>", unsafe_allow_html=True)

        injection_time = st.number_input("Injection_Time", value=feature_means['Injection_Time'])
        plasticizing_time = st.number_input("Plasticizing_Time", value=feature_means['Plasticizing_Time'])
        cycle_time = st.number_input("Cycle_Time", value=feature_means['Cycle_Time'])
        avg_screw_rpm = st.number_input("Average_Screw_RPM", value=feature_means['Average_Screw_RPM'])
        max_switch_over_pressure = st.number_input("Max_Switch_Over_Pressure", value=feature_means['Max_Switch_Over_Pressure'])
        avg_back_pressure = st.number_input("Average_Back_Pressure", value=feature_means['Average_Back_Pressure'])
        mold_temp_4 = st.number_input("Mold_Temperature_4", value=feature_means['Mold_Temperature_4'])
        max_injection_speed = st.number_input("Max_Injection_Speed", value=feature_means['Max_Injection_Speed'])
        hopper_temp = st.number_input("Hopper_Temperature", value=feature_means['Hopper_Temperature'])
        barrel_temp_1 = st.number_input("Barrel_Temperature_1", value=feature_means['Barrel_Temperature_1'])

    # 결과 영역
    with main_col2:
        if predict_button:
            injection_rate, avg_material_temp = calculate_derived_features(max_injection_speed, hopper_temp, barrel_temp_1)

            input_data = [
                injection_time, plasticizing_time, cycle_time, avg_screw_rpm,
                max_switch_over_pressure, avg_back_pressure, mold_temp_4,
                injection_rate, avg_material_temp
            ]

            pred = cn7_model.predict(np.array(input_data).reshape(1, -1))

            if pred[0] == 1:
                top_col1, top_col2 = st.columns([5, 5])

                with top_col1:
                    st.markdown("<h2 style='color:red;'>❌ DEFECT <span style='font-size:20px;'>(불량 발생)</span></h2>", unsafe_allow_html=True)

                    feature_cols = ['Injection_Time', 'Plasticizing_Time', 'Cycle_Time',
                                    'Average_Screw_RPM', 'Max_Switch_Over_Pressure', 'Average_Back_Pressure',
                                    'Mold_Temperature_4', 'Injection_Rate_Calc', 'Avg_Material_Temp']

                    data['Injection_Rate_Calc'] = 63.62 * (data['Max_Injection_Speed'] / 10)
                    data['Avg_Material_Temp'] = (data['Hopper_Temperature'] + data['Barrel_Temperature_1']) / 2

                    distances = euclidean_distances(data[feature_cols], np.array(input_data).reshape(1, -1))
                    nearest_idx = np.argmin(distances)
                    reason = data.iloc[nearest_idx]['Reason']

                    if reason in reason_images:
                        st.image(f"images/{reason_images[reason]}", width=600)

                    st.markdown(f"<div style='border: 2px solid #f0f0f0; padding: 10px; border-radius: 10px; margin-bottom: 30px;'>"
                                f"<p style='font-size:18px;'><b>불량 원인 : </b> <span style='color:red'>{reason}</span></p>"
                                f"<p style='color:red; font-size:16px;'>⚠️ "
                                f"{'공정 조건 미확립, 금형/설비 세팅 오류' if reason == '초기허용불량' else ('금형 내 가스 배출 불량, 수지 수분 과다 가능성' if reason == '가스' else '금형 내 수지 충전 부족')}"
                                f"</p>"
                                f"<p style='color:blue; font-size:16px;'>✅ "
                                f"{'초기 샘플링 검사 강화 필요' if reason == '초기허용불량' else ('가스 배출구 확인 및 사출 조건 조정 필요' if reason == '가스' else '사출 속도, 압력, 온도 조건 재점검 필요')}"
                                f"</p></div>", unsafe_allow_html=True)

                    feature_names = feature_cols
                    importances = cn7_model.feature_importances_
                    top4_idx = np.argsort(importances)[::-1][:4]
                    top4_features = [feature_names[i] for i in top4_idx]

                    st.markdown("<div style='background-color:#fffde7;padding:5px 16px;border-radius:10px; margin-top: 10px;'><b style='font-size:20px;'>주요 원인 TOP 4</b></div>", unsafe_allow_html=True)
                    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
                    for i, feat in enumerate(top4_features, 1):
                        st.markdown(f"<p style='font-size:20px;margin-left:10px;'>{i}. {feat}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with top_col2:
                    st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 20px; margin-bottom: 20px; '><b style='font-size:20px;'>누적 불량률</b></div>", unsafe_allow_html=True)

                    # 누적 불량률 박스 (배경 흰색)
                    with st.container():
                        defect_counts_total = labeled_data['PassOrFail'].value_counts()
                        sizes = [defect_counts_total['N'], defect_counts_total['Y']]
                        labels = ['불량품', '양품']
                        colors = ['#FF6B6B', '#4dabf7']
                        total_pct = sizes[0] / sum(sizes) * 100

                        fig = go.Figure(data=[go.Pie(
                            labels=labels,
                            values=sizes,
                            hole=0.7,
                            marker_colors=colors,
                            textinfo='none'
                        )])

                        fig.update_layout(
                            showlegend=False,
                            annotations=[dict(text=f"{total_pct:.1f}%", x=0.5, y=0.5, font_size=40, showarrow=False, font_color='red')],
                            margin=dict(l=10, r=10, t=10, b=10),
                            paper_bgcolor="white",
                            plot_bgcolor="white",
                            width=250,
                            height=250
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    # 불량 원인 분포
                    defect_counts = labeled_data[(labeled_data['PassOrFail'] == 'N') & (labeled_data['Reason'].notnull())]['Reason'].value_counts(normalize=True) * 100

                    st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 70px; margin-bottom: 20px;'><b style='font-size:20px;'>불량 원인 분포</b></div>", unsafe_allow_html=True)
                    fig, ax = plt.subplots()
                    bars = ax.barh(defect_counts.index, defect_counts.values, color='#c1f0c1')
                    ax.set_xlim(0, 100)
                    ax.set_xlabel('%', fontsize=14, fontproperties=font_prop)
                    ax.set_yticklabels(defect_counts.index, fontsize=16, fontweight='bold', fontproperties=font_prop)

                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                                f'{width:.2f}%', va='center', color='black', fontsize=16, fontweight='bold', fontproperties=font_prop)

                    st.pyplot(fig)

                st.write("---")
                st.subheader("개선 가이드")

                # ✅ 양품 데이터에서 파생 변수 생성
                good_data = labeled_data[labeled_data['PassOrFail'] == 'Y'].copy()
                good_data['Injection_Rate_Calc'] = 63.62 * (good_data['Max_Injection_Speed'] / 10)
                good_data['Avg_Material_Temp'] = (good_data['Hopper_Temperature'] + good_data['Barrel_Temperature_1']) / 2

                # ✅ 중요 피처 목록과 중요도 추출
                feature_cols = ['Injection_Time', 'Plasticizing_Time', 'Cycle_Time',
                                'Average_Screw_RPM', 'Max_Switch_Over_Pressure', 'Average_Back_Pressure',
                                'Mold_Temperature_4', 'Injection_Rate_Calc', 'Avg_Material_Temp']
                importances = cn7_model.feature_importances_
                top4_idx = np.argsort(importances)[::-1][:4]
                top4_features = [feature_cols[i] for i in top4_idx]

                # ✅ 아이콘 매핑 (영문 컬럼명에 이모지 대응)
                feature_icons = {
                    'Injection_Time': '🕓',
                    'Plasticizing_Time': '🧪',
                    'Cycle_Time': '⏱️',
                    'Average_Screw_RPM': '🔁',
                    'Max_Switch_Over_Pressure': '⚙️',
                    'Average_Back_Pressure': '💨',
                    'Mold_Temperature_4': '🌡️',
                    'Injection_Rate_Calc': '🔥',
                    'Avg_Material_Temp': '🌡️'
                }

                # ✅ 현재 입력값으로 파생 변수 포함한 딕셔너리 구성
                injection_rate, avg_material_temp = calculate_derived_features(max_injection_speed, hopper_temp, barrel_temp_1)
                input_dict = {
                    'Injection_Time': injection_time,
                    'Plasticizing_Time': plasticizing_time,
                    'Cycle_Time': cycle_time,
                    'Average_Screw_RPM': avg_screw_rpm,
                    'Max_Switch_Over_Pressure': max_switch_over_pressure,
                    'Average_Back_Pressure': avg_back_pressure,
                    'Mold_Temperature_4': mold_temp_4,
                    'Injection_Rate_Calc': injection_rate,
                    'Avg_Material_Temp': avg_material_temp
                }

                # ✅ 카드 표시 (2열)
                col3, col4 = st.columns(2)

                for i, feature in enumerate(top4_features):
                    current_value = input_dict[feature]
                    target_value = good_data[feature].median()
                    icon = feature_icons[feature]

                    if round(current_value, 2) == round(target_value, 2):
                        arrow = ""
                        status_note = "<span style='color:#2f54eb; font-size:14px; font-weight:bold;'>✔ 조정 필요 없음</span>"
                    else:
                        arrow = "🔼" if target_value > current_value else "🔽"
                        status_note = ""

                    card_html = f"""
                    <div style=\"background-color:#f9f9f9; border:1px solid #ddd; border-radius:10px;
                                padding:20px 14px; margin-bottom:12px; box-shadow: 1px 1px 4px rgba(0,0,0,0.03);
                                height: 100px; display: flex; flex-direction: column; justify-content: center;\">
                        <div style=\"display: flex; justify-content: space-between; align-items: center;\">
                            <div style=\"font-size:16px; font-weight:bold;\">{icon} {feature}</div> 
                            <div style=\"font-size:15px; color:#333;\">
                                {current_value:.2f} → 
                                <span style=\"color:#2b8a3e; font-weight:bold;\">{target_value:.2f} {arrow}</span>
                                <br>{status_note}
                            </div>
                        </div>
                    </div>
                    """

                    if i % 2 == 0:
                        with col3:
                            st.markdown(card_html, unsafe_allow_html=True)
                    else:
                        with col4:
                            st.markdown(card_html, unsafe_allow_html=True)

            else:
                # ================= 정상 생산 ================= #
                st.success("✅ 정상 생산")

                # 📈 공정 상태 메시지
                st.markdown("📈 현재 입력된 조건은 정상 범위 내에 있으며, 공정이 안정적으로 운영되고 있습니다.")

                # 🔧 예방 점검 제안
                st.markdown("""
                <div style='border: 1px solid #d9f7be; background-color: #f6ffed; padding: 10px 16px; border-radius: 10px; margin-top: 15px;'>
                    <b>🔧 예방 점검 제안:</b><br>
                    ✔ 금형 냉각 유로 점검<br>
                    ✔ 재료 건조기 수분 센서 확인<br>
                    ✔ 스크류 마모 상태 정기 점검
                </div>
                """, unsafe_allow_html=True)

                # 📊 관리도 (Control Chart)
                st.markdown(
                    "<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 30px; margin-bottom: 10px;'>"
                    "<b style='font-size:20px;'>관리도 (Control Chart)</b></div>",
                    unsafe_allow_html=True
                )

                import datetime
                import plotly.graph_objects as go
                
                # 관리도용 데이터 별도 불러오기
                labeled_total = pd.read_csv("labeled_data.csv")

                labeled_total['TimeStamp'] = pd.to_datetime(labeled_total['TimeStamp'])
                filtered = labeled_total[(labeled_total['EQUIP_NAME'].str.contains("우진2호기")) &
                                        (labeled_total['PART_NAME'].str.contains("CN7"))].copy()
                filtered['Date'] = filtered['TimeStamp'].dt.date

                daily_stats = filtered.groupby("Date")["PassOrFail"].value_counts().unstack().fillna(0)
                daily_stats["DefectRate"] = daily_stats["N"] / (daily_stats["Y"] + daily_stats["N"]) * 100
                daily_stats = daily_stats.reset_index()[["Date", "DefectRate"]]

                x = daily_stats["Date"]
                y = daily_stats["DefectRate"]
                mean = y.mean()
                std = y.std()

                fig_line = go.Figure()
                fig_line.add_trace(go.Scatter(
                    x=x,
                    y=y,
                    mode='markers+lines',
                    name='불량률',
                    line=dict(width=2, color='black'),
                    marker=dict(size=6, color='black')
                ))

                for sigma, color, name in [(1, '#d9fdd3', 'Zone C'), (2, '#fffacc', 'Zone B'), (3, '#ffe1e1', 'Zone A')]:
                    fig_line.add_shape(type="rect", x0=min(x), x1=max(x),
                        y0=mean - sigma*std, y1=mean - (sigma-1)*std if sigma > 1 else mean,
                        fillcolor=color, line=dict(width=0), opacity=0.5)
                    fig_line.add_shape(type="rect", x0=min(x), x1=max(x),
                        y0=mean + (sigma-1)*std if sigma > 1 else mean, y1=mean + sigma*std,
                        fillcolor=color, line=dict(width=0), opacity=0.5)

                fig_line.add_hline(y=mean, line=dict(color='blue', width=1, dash='dot'))

                fig_line.update_layout(
                    yaxis_title='불량률 (%)',
                    xaxis_title='생산일자',
                    margin=dict(l=10, r=10, t=10, b=10),
                    height=350,
                    paper_bgcolor='white',
                    plot_bgcolor='white',
                    showlegend=False
                )
                st.plotly_chart(fig_line, use_container_width=True)

                col_defect, col_reason = st.columns(2)

                with col_defect:
                    st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 20px; margin-bottom: 20px;'><b style='font-size:20px;'>누적 불량률</b></div>", unsafe_allow_html=True)
                    defect_counts_total = labeled_data['PassOrFail'].value_counts()
                    sizes = [defect_counts_total['N'], defect_counts_total['Y']]
                    labels = ['불량품', '양품']
                    colors = ['#FF6B6B', '#4dabf7']
                    total_pct = sizes[0] / sum(sizes) * 100

                    fig = go.Figure(data=[go.Pie(
                        labels=labels,
                        values=sizes,
                        hole=0.7,
                        marker_colors=colors,
                        textinfo='none'
                    )])

                    fig.update_layout(
                        showlegend=False,
                        annotations=[dict(text=f"{total_pct:.1f}%", x=0.5, y=0.5, font_size=40, showarrow=False, font_color='red')],
                        margin=dict(l=10, r=10, t=10, b=10),
                        paper_bgcolor="white",
                        plot_bgcolor="white",
                        width=250,
                        height=250
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col_reason:
                    st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 20px; margin-bottom: 20px;'><b style='font-size:20px;'>불량 원인 분포</b></div>", unsafe_allow_html=True)
                    defect_counts = labeled_data[(labeled_data['PassOrFail'] == 'N') & (labeled_data['Reason'].notnull())]['Reason'].value_counts(normalize=True) * 100

                    fig, ax = plt.subplots()
                    bars = ax.barh(defect_counts.index, defect_counts.values, color='#c1f0c1')
                    ax.set_xlim(0, 100)
                    ax.set_xlabel('%', fontsize=14)
                    ax.set_yticklabels(defect_counts.index, fontsize=16, fontweight='bold')

                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                                f'{width:.2f}%', va='center', color='black', fontsize=16, fontweight='bold')

                    st.pyplot(fig)