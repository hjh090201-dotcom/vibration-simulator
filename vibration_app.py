import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib as mpl
import os

# ===============================
# 한글 폰트 자동 설정 (Streamlit Cloud 대응)
# ===============================
font_path = None

possible_fonts = [
    "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
    "/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
]

for f in possible_fonts:
    if os.path.exists(f):
        font_path = f
        break

if font_path:
    font_prop = fm.FontProperties(fname=font_path)
    mpl.rcParams["font.family"] = font_prop.get_name()

mpl.rcParams["axes.unicode_minus"] = False

# ===============================
# Streamlit 페이지 설정
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

# ===============================
# 초기화
# ===============================
x = np.zeros(len(t))
v = np.zeros(len(t))
x[0] = x0

# ===============================
# 진동 시뮬레이션
# ===============================
for i in range(1, len(t)):
    F_spring = -k * x[i - 1]
    F_damper = -c * v[i - 1]
    a = (F_spring + F_damper) / m

    v[i] = v[i - 1] + a * dt
    x[i] = x[i - 1] + v[i] * dt

# ===============================
# 그래프
# ===============================
with col1:
    st.header("진동 그래프")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, x)

    ax.set_title("질량-스프링-댐퍼 시스템의 진동")
    ax.set_xlabel("시간 (s)")
    ax.set_ylabel("변위 (m)")
    ax.grid(True)

    st.pyplot(fig)



