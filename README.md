# 🏭 사출성형 불량 예측 대시보드 (Injection Molding Defect Prediction Dashboard)

이 대시보드는 사출성형 공정 데이터를 기반으로 자동차 부품의 불량 발생 여부를 예측하고, 주요 원인 분석 및 개선 가이드를 시각적으로 제공합니다.  
Streamlit 기반의 인터페이스를 통해 작업자가 사전에 공정 진단과 피드백을 받을 수 있도록 설계되었습니다.

## 🔧 주요 기능
- 📊 불량 예측: 사용자가 입력한 공정 조건으로 불량 발생 여부를 예측
- 🔍 주요 원인 분석: 예측된 불량의 주요 공정 원인 Top 4~6 항목 제시
- 🧭 개선 가이드: 실제 양품 데이터를 기준으로 변수 조정 방향 제안
- 📈 불량률 및 원인 분포 시각화: 누적 불량률, 일별/월별 불량 트렌드, 관리도 포함

## 🧪 대상 데이터 및 모델
- 대상 부품: CN7 (Avante), RG3 (Genesis G80)
- 사용 모델: XGBoost
- 데이터: 사출속도, 금형온도, 백압, 사이클타임 등 주요 공정 변수 포함

## 🚀 데모 바로가기
[👉 대시보드 실행](https://injection-molding-dashboard-ez6alk9qjkn6hndnrfuai8.streamlit.app/)

## ⚙️ 사용 기술
- Python (Pandas, NumPy, Scikit-learn, XGBoost)
- Streamlit
- Plotly / Matplotlib (시각화)
- GitHub + Streamlit Cloud (배포)

---

# 🏭 Injection Molding Defect Prediction Dashboard

This Streamlit dashboard predicts defect occurrences in automotive injection molding processes 
and provides visual explanations of key contributing factors and actionable improvement guides based on user-defined process inputs.

## 🔧 Key Features
- 📊 Defect Prediction: Predicts whether a part will be defective based on process conditions
- 🔍 Root Cause Analysis: Displays Top 4–6 most important features contributing to defect
- 🧭 Improvement Guide: Suggests directions for optimization using good sample statistics
- 📈 Visual Insights: Cumulative defect rates, defect cause distribution, control charts, and trends

## 🧪 Dataset & Models
- Target parts: CN7 (Avante), RG3 (Genesis G80)
- ML Model: XGBoost
- Process variables: injection speed, mold temperature, back pressure, cycle time, etc.

## 🚀 Live Demo
[👉 Launch Dashboard](https://injection-molding-dashboard-ez6alk9qjkn6hndnrfuai8.streamlit.app/)

## ⚙️ Tech Stack
- Python (Pandas, NumPy, Scikit-learn, XGBoost)
- Streamlit
- Plotly / Matplotlib
- GitHub + Streamlit Cloud
