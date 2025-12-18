import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# 한글 폰트 설정 (윈도우)
# ===============================
plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

# ===============================
# 제목
# ===============================
st.title("질량-스프링-댐퍼 진동 시뮬레이터")

# ===============================
# 화면 좌우 분할
# ===============================
col_graph, col_control = st.columns([3, 1])

# ===============================
# 오른쪽: 변수 조절
# ===============================
with col_control:
    st.header("변수 조절")

    m = st.slider("질량 (kg)", 0.1, 5.0, 1.0)
    k = st.slider("스프링 상수 (N/m)", 1.0, 50.0, 10.0)
    c = st.slider("감쇠 계수 (Ns/m)", 0.0, 5.0, 0.5)
    x0 = st.slider("초기 변위 (m)", 0.1, 2.0, 1.0)

    # 이론값 표시
    omega_n = np.sqrt(k / m)
    zeta = c / (2 * np.sqrt(m * k))

    st.markdown("---")
    st.write(f"고유진동수 ωₙ = {omega_n:.2f} rad/s")
    st.write(f"감쇠비 ζ = {zeta:.2f}")

    if zeta < 1:
        st.write("👉 언더댐핑 (진동 발생)")
    elif zeta == 1:
        st.write("👉 임계 감쇠")
    else:
        st.write("👉 오버댐핑 (진동 없음)")

# ===============================
# 시간 설정
# ===============================
dt = 0.01
t = np.arange(0, 10, dt)

# ===============================
# 초기값
# ===============================
x = np.zeros(len(t))
v = np.zeros(len(t))

x[0] = x0
v[0] = 0.0

# ===============================
# 진동 계산 (수치해석)
# ===============================
for i in range(1, len(t)):
    F_spring = -k * x[i-1]
    F_damper = -c * v[i-1]
    F_total = F_spring + F_damper

    a = F_total / m
    v[i] = v[i-1] + a * dt
    x[i] = x[i-1] + v[i] * dt

# ===============================
# 왼쪽: 그래프 출력
# ===============================
with col_graph:
    st.header("진동 그래프")

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(t, x)

    ax.set_xlabel("시간 (s)")
    ax.set_ylabel("변위 (m)")
    ax.set_title("질량-스프링-댐퍼 시스템의 진동 응답")

    ax.set_xlim(0, 10)
    ax.set_xticks(np.arange(0, 11, 1))

    ax.set_ylim(-1.5, 1.5)
    ax.set_yticks(np.arange(-1.5, 1.6, 0.5))

    ax.grid(True)
    st.pyplot(fig)
