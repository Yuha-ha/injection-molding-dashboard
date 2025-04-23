def render() :
    import streamlit as st
    import pickle
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    import plotly.graph_objects as go
    import matplotlib
    import datetime
    from sklearn.metrics.pairwise import euclidean_distances
    import matplotlib.font_manager as fm

    font_path = "fonts/NanumGothicCoding.ttf"  # 상대 경로
    font_prop = fm.FontProperties(fname=font_path, size=16, weight='bold')
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rcParams['axes.unicode_minus'] = False

    # 모델 & 데이터 로드
    with open('rg3_xgb_model.pkl', 'rb') as f:
        rg3_model = pickle.load(f)

    data = pd.read_csv('Combined_Dataset_with_300_Synthetic_Fails.csv')
    labeled_data = pd.read_csv("labeled_rg3.csv")

    # 모델 학습에 사용된 피처
    features = [
        'Average_Screw_RPM', 'Cycle_Time', 'Clamp_Close_Time',
        'Barrel_Temperature_1', 'Barrel_Temperature_6',
        'Mean_Mold_Temp', 'Filling_Ratio',
        'Avg_Back_Pressure_Ratio', 'Avg_Material_Temp'
    ]

    # 파생 변수 생성을 위한 입력 컬럼
    input_cols = [
        'Average_Screw_RPM', 'Cycle_Time', 'Clamp_Close_Time',
        'Barrel_Temperature_1', 'Barrel_Temperature_6',
        'Mold_Temperature_3', 'Mold_Temperature_4',
        'Filling_Time', 'Injection_Time',
        'Average_Back_Pressure', 'Max_Back_Pressure',
        'Hopper_Temperature'
    ]

    feature_means = data[input_cols].mean().to_dict()

    reason_images = {
        '가스': 'reason2.png',
        '미성형': 'reason3.png'
    }

    col1, col2 = st.columns([7, 1])  # 비율은 조정 가능

    with col1:
        st.markdown("<h1 style='text-align: left;'>Genesis G80 (RG3) 불량 예측 대시보드</h1>", unsafe_allow_html=True)

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
        user_inputs = {}
        for col in input_cols:
            user_inputs[col] = st.number_input(col, value=float(feature_means[col]))
        
        # 파생 변수 계산
        user_inputs['Mean_Mold_Temp'] = (user_inputs['Mold_Temperature_3'] + user_inputs['Mold_Temperature_4']) / 2
        user_inputs['Filling_Ratio'] = user_inputs['Filling_Time'] / user_inputs['Injection_Time'] if user_inputs['Injection_Time'] else 0
        user_inputs['Avg_Back_Pressure_Ratio'] = user_inputs['Average_Back_Pressure'] / user_inputs['Max_Back_Pressure'] if user_inputs['Max_Back_Pressure'] else 0
        user_inputs['Avg_Material_Temp'] = (user_inputs['Hopper_Temperature'] + user_inputs['Barrel_Temperature_1']) / 2        
        
    # 결과 영역
    with main_col2:
        if predict_button:
            input_data = [user_inputs[col] for col in features]
            pred = rg3_model.predict(np.array(input_data).reshape(1, -1))

            if pred[0] == 1:
                top_col1, top_col2 = st.columns([5, 5])

                with top_col1:
                    st.markdown("<h2 style='color:red;'>❌ DEFECT <span style='font-size:20px;'>(불량 발생)</span></h2>", unsafe_allow_html=True)

                    feature_cols = features
                    defect_data = data[data['PassOrFail'] == 'N'].copy()
                    distances = euclidean_distances(defect_data[feature_cols], np.array(input_data).reshape(1, -1))
                    nearest_idx = np.argmin(distances)
                    reason = defect_data.iloc[nearest_idx]['Reason']

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

                    importances = rg3_model.feature_importances_
                    top6_idx = np.argsort(importances)[::-1][:6]
                    top6_features = [feature_cols[i] for i in top6_idx]

                    st.markdown("<div style='background-color:#fffde7;padding:5px 16px;border-radius:10px; margin-top: 10px;'><b style='font-size:20px;'>주요 원인 TOP 6</b></div>", unsafe_allow_html=True)
                    st.markdown("<div style='margin-top: 20px;'>", unsafe_allow_html=True)
                    for i, feat in enumerate(top6_features, 1):
                        st.markdown(f"<p style='font-size:20px;margin-left:10px;'>{i}. {feat}</p>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with top_col2:
                    st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 20px; margin-bottom: 20px; '><b style='font-size:20px;'>누적 불량률</b></div>", unsafe_allow_html=True)

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

                    defect_counts = labeled_data[(labeled_data['PassOrFail'] == 'N') & (labeled_data['Reason'].notnull())]['Reason'].value_counts(normalize=True) * 100

                    st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 45px; margin-bottom: 20px;'><b style='font-size:20px;'>불량 원인 분포</b></div>", unsafe_allow_html=True)
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

                good_data = labeled_data[labeled_data['PassOrFail'] == 'Y'].copy()
                top6_features = [feature_cols[i] for i in top6_idx]

                feature_icons = {
                    'Average_Screw_RPM': '🔁', 'Cycle_Time': '⏱️', 'Clamp_Close_Time': '🔒',
                    'Barrel_Temperature_1': '🌡️', 'Barrel_Temperature_6': '🌡️',
                    'Mean_Mold_Temp': '❄️', 'Filling_Ratio': '💧',
                    'Avg_Back_Pressure_Ratio': '📊', 'Avg_Material_Temp': '🔥'
                }

                input_dict = {k: user_inputs[k] for k in top6_features}

                col3, col4 = st.columns(2)

                for i, feature in enumerate(top6_features):
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
                                padding:20px 14px; margin-bottom:12px; box-shadow: 1px 1px 4px rgba(0,0,0,0.03);\">
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
                st.success("✅ 정상 생산")
                st.markdown("📈 현재 입력된 조건은 정상 범위 내에 있으며, 공정이 안정적으로 운영되고 있습니다.")

                st.markdown("""
                    <div style='border: 1px solid #d9f7be; background-color: #f6ffed; padding: 10px 16px; border-radius: 10px; margin-top: 15px;'>
                        <b>🔧 예방 점검 제안:</b><br>
                        ✔ 금형 냉각 유로 점검<br>
                        ✔ 재료 건조기 수분 센서 확인<br>
                        ✔ 스크류 마모 상태 정기 점검
                    </div>
                """, unsafe_allow_html=True)

                # 관리도 추가 (650 우진2호기 & RG3만 필터)
                st.markdown("<div style='background-color:#f0f0f0;padding:5px 16px;border-radius:10px; margin-top: 30px;'><b style='font-size:20px;'>관리도 (Control Chart)</b></div>", unsafe_allow_html=True)

                # 관리도용 데이터 별도 불러오기
                labeled_total = pd.read_csv("labeled_data.csv")

                labeled_total['TimeStamp'] = pd.to_datetime(labeled_total['TimeStamp'])
                filtered = labeled_total[
                labeled_total['EQUIP_NAME'].str.contains("650.*우진2호기") &
                labeled_total['PART_NAME'].str.contains("RG3")
                ].copy()
                filtered['Date'] = filtered['TimeStamp'].dt.date

                daily_stats = filtered.groupby("Date")["PassOrFail"].value_counts().unstack().fillna(0)
                if 'N' in daily_stats.columns and 'Y' in daily_stats.columns:
                    daily_stats["DefectRate"] = daily_stats["N"] / (daily_stats["Y"] + daily_stats["N"]) * 100
                else:
                    daily_stats["DefectRate"] = 0
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
                    ax.set_xlabel('%', fontsize=14, fontproperties=font_prop)
                    ax.set_yticklabels(defect_counts.index, fontsize=16, fontweight='bold', fontproperties=font_prop)

                    for bar in bars:
                        width = bar.get_width()
                        ax.text(width + 1, bar.get_y() + bar.get_height()/2,
                                f'{width:.2f}%', va='center', color='black', fontsize=16, fontweight='bold', fontproperties=font_prop)

                    st.pyplot(fig)