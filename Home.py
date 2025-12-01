import streamlit as st

st.set_page_config(page_title="AI Deadlock Detection", page_icon="🤖", layout="wide")

# 🎨 CUSTOM CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .hero-title {
            text-align: center; font-size: 3.5rem; font-weight: 800;
            background: linear-gradient(90deg, #2563eb 0%, #7c3aed 100%);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }
        .hero-subtitle { text-align: center; font-size: 1.2rem; color: #4b5563; margin-bottom: 30px; }
        
        .feature-card {
            background-color: white; padding: 20px; border-radius: 12px;
            border: 1px solid #e5e7eb; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center; height: 100%; transition: transform 0.2s;
        }
        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
        .feature-icon { font-size: 2.5rem; margin-bottom: 15px; }
        .feature-title { font-weight: 700; color: #1f2937; margin-bottom: 10px; }
        
        .status-badge {
            background-color: #dcfce7; color: #166534; padding: 5px 15px;
            border-radius: 20px; font-weight: bold; border: 1px solid #86efac;
        }
        
        div.stButton > button {
            background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
            color: white; border: none; border-radius: 0.5rem; padding: 0.75rem 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# HERO
st.markdown('<h1 class="hero-title">AI-Powered Deadlock Detection</h1>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Operating Systems CA2 Project</div>', unsafe_allow_html=True)



st.markdown("---")

# FEATURES
st.subheader("🚀 Features")
c1, c2, c3, c4 = st.columns(4)

def feature_card(icon, title, desc):
    return f"""
    <div class="feature-card">
        <div class="feature-icon">{icon}</div>
        <div class="feature-title">{title}</div>
        <div style="font-size:0.9rem; color:#6b7280;">{desc}</div>
    </div>
    """

with c1: st.markdown(feature_card("⚙️", "Simulation", "OS Process-Resource Simulation"), unsafe_allow_html=True)
with c2: st.markdown(feature_card("📐", "Algorithm", "Banker's Algorithm Logic"), unsafe_allow_html=True)
with c3: st.markdown(feature_card("🤖", "AI Model", "Random Forest Prediction"), unsafe_allow_html=True)
with c4: st.markdown(feature_card("📊", "Analysis", "Compare Accuracy"), unsafe_allow_html=True)

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

