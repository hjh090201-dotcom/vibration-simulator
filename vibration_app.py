import streamlit as st
import numpy as np
import pandas as pd
import altair as alt

# ===============================
# 페이지 설정
# ===============================
st.set_page_config(layout="wide")
st.title("질량-스프링-댐퍼 진동 시뮬레이터")

# ===============================
# 레이아웃
# ===============================
col1, col2 = st.columns([2, 1])

with col2:
    st.header("변수 조절")

    m = st.slider("질량 (kg)", 0.1, 5.0, 1.0, 0.1)
    k = st.slider("스프링 상수 (N/m)", 1.0, 50.0, 10.0, 1.0)
    c = st.slider("감쇠 계수 (Ns/m)", 0.0, 5.0, 0.5, 0.1)
    x0 = st.slider("초기 변위 (m)", -2.0, 2.0, 1.0, 0.1)

# ===============================
# 시간 설정
# ===============================
t_max = 10
dt = 0.01
t = np.arange(0, t_max, dt)

x = np.zeros(len(t))
v = np.zeros(len(t))
x[0] = x0

# ===============================
# 진동 시뮬레이션
# ===============================
for i in range(1, len(t)):
    F_spring = -k * x[i-1]
    F_damper = -c * v[i-1]
    a = (F_spring + F_damper) / m

    v[i] = v[i-1] + a * dt
    x[i] = x[i-1] + v[i] * dt

# ===============================
# 데이터프레임
# ===============================
df = pd.DataFrame({
    "시간 (s)": t,
    "변위 (m)": x
})

# ===============================
# 그래프 (Altair)
# ===============================
with col1:
    st.header("진동 그래프")

    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(
            x=alt.X("시간 (s)", title="시간 (s)"),
            y=alt.Y("변위 (m)", title="변위 (m)")
        )
        .properties(
            title="질량-스프링-댐퍼 시스템의 진동",
            width=700,
            height=400
        )
    )

    st.altair_chart(chart, use_container_width=True)





