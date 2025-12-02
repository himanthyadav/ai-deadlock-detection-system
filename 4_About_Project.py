import streamlit as st

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="wide")


st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .info-card {
            background-color: white; padding: 25px; border-radius: 12px;
            border: 1px solid #e5e7eb; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); height: 100%;
        }
        .team-card {
            background: linear-gradient(135deg, #f8fafc 0%, #eef2ff 100%);
            border: 1px solid #c7d2fe; border-radius: 15px; padding: 20px;
            text-align: center; transition: transform 0.2s;
        }
        .team-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
        .team-name { font-size: 1.2rem; font-weight: 800; color: #1e3a8a; margin-top: 10px; }
        .tech-badge {
            display: inline-block; background-color: #e0e7ff; color: #3730a3;
            padding: 6px 12px; border-radius: 20px; font-weight: 600; margin: 5px; font-size: 0.9rem;
        }
    </style>
""", unsafe_allow_html=True)

st.title("ℹ️ About the Project")
st.markdown("#### 🤖 AI-Powered Deadlock Detection System | **OS CA2 Project**")
st.markdown("This project bridges the gap between **Operating Systems** and **Artificial Intelligence**.")
st.markdown("---")

st.subheader("👨‍💻 Project Team")
col1, col2, col3 = st.columns(3)

def team_card(name, reg_id, icon="🧑‍🎓"):
    return f"""
    <div class="team-card">
        <div style="font-size: 3rem;">{icon}</div>
        <div class="team-name">{name}</div>
        <div style="font-size: 0.9rem; color: #6b7280;">ID: {reg_id}</div>
    </div>
    """

with col1: st.markdown(team_card("Himanth", "12414121", "👨‍💻"), unsafe_allow_html=True)
with col2: st.markdown(team_card("Sushmitha", "12412139", "👩‍💻"), unsafe_allow_html=True)
with col3: st.markdown(team_card("Anjana Karthik", "12411006", "👨‍💻"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1:
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("🎯 Objectives")
        st.markdown("""
        1. Simulate OS Processes.
        2. Implement Classical Deadlock Detection.
        3. Train AI Model (Random Forest).
        4. Predict & Compare Results.
        """)
        st.markdown('</div>', unsafe_allow_html=True)
with c2:
    with st.container():
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("🧩 Overview")
        st.markdown("""
        * **Simulation:** Core OS Algorithm.
        * **AI Prediction:** ML Training.
        * **Comparison:** Math vs AI.
        """)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("🛠️ Tech Stack")
st.markdown("""
    <span class="tech-badge">🐍 Python</span>
    <span class="tech-badge">🌊 Streamlit</span>
    <span class="tech-badge">🔢 NumPy</span>
    <span class="tech-badge">🤖 Scikit-Learn</span>

""", unsafe_allow_html=True)
