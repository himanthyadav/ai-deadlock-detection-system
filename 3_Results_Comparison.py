import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Results Comparison", page_icon="📊", layout="wide")

# 🎨 CUSTOM CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

        .badge-safe {
            background-color: #d1fae5; color: #065f46; padding: 8px 16px;
            border-radius: 50px; font-weight: 800; font-size: 1.2rem;
            display: inline-block; margin-bottom: 10px;
        }
        .badge-dead {
            background-color: #fee2e2; color: #991b1b; padding: 8px 16px;
            border-radius: 50px; font-weight: 800; font-size: 1.2rem;
            display: inline-block; margin-bottom: 10px;
        }
        .stDataFrame { border: 1px solid #e5e7eb; border-radius: 8px; }
    </style>
""", unsafe_allow_html=True)

# -------- LOGIC --------
def detect_deadlock(total_resources, allocation, request):
    total = np.array(total_resources, dtype=int)
    alloc = np.array(allocation, dtype=int)
    req = np.array(request, dtype=int)
    n_proc, n_res = alloc.shape
    work = total - alloc.sum(axis=0)
    finish = np.array([False] * n_proc)
    changed = True
    while changed:
        changed = False
        for i in range(n_proc):
            if not finish[i] and np.all(req[i] <= work):
                work = work + alloc[i]
                finish[i] = True
                changed = True
    return bool((~finish).any())

# -------- UI --------
st.title("📊 Results Comparison")
st.markdown("Compare the **Classical Algorithm** against the **AI Prediction Model**.")
st.markdown("---")

if "last_state" not in st.session_state:
    st.warning("⚠️ No simulation data found. Please run **Deadlock Simulation** first.")
    st.stop()

last = st.session_state["last_state"]
total = np.array(last["total"])
alloc = np.array(last["alloc"])
req = np.array(last["req"])
n, m = alloc.shape

# 1. Snapshot
with st.container(border=True):
    st.subheader("1️⃣ System Snapshot")
    st.write("**Total Resources:**")
    cols = st.columns(len(total))
    for i, val in enumerate(total):
        cols[i].metric(f"R{i}", val)
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.caption("Allocation")
        st.dataframe(pd.DataFrame(alloc, columns=[f"R{j}" for j in range(m)]), use_container_width=True)
    with c2:
        st.caption("Request")
        st.dataframe(pd.DataFrame(req, columns=[f"R{j}" for j in range(m)]), use_container_width=True)

# 2. Comparison
st.markdown("---")
st.subheader("2️⃣ Algorithm vs. AI")

# Calc
classical_deadlock = detect_deadlock(total, alloc, req)

ai_result = None
ai_proba = None
ai_error = None
if "deadlock_model" not in st.session_state:
    ai_error = "Model not trained yet."
else:
    model = st.session_state["deadlock_model"]
    feat_dim = st.session_state.get("feature_dim", None)
    features = np.concatenate([total.flatten(), alloc.flatten(), req.flatten()]).reshape(1, -1)
    if feat_dim is not None and features.shape[1] != feat_dim:
        ai_error = "Dimension mismatch. Retrain model."
    else:
        pred = int(model.predict(features)[0])
        proba = model.predict_proba(features)[0][1]
        ai_result = bool(pred)
        ai_proba = proba

c_classic, c_ai = st.columns(2)

with c_classic:
    with st.container(border=True):
        st.markdown("### 📐 Classical Algorithm")
        st.caption("Banker's Algorithm (Exact)")
        st.markdown("<br>", unsafe_allow_html=True)
        if classical_deadlock:
            st.markdown('<div style="text-align:center"><span class="badge-dead">DEADLOCK</span></div>', unsafe_allow_html=True)
            st.error("Cycle detected.")
        else:
            st.markdown('<div style="text-align:center"><span class="badge-safe">SAFE STATE</span></div>', unsafe_allow_html=True)
            st.success("Safe sequence exists.")

with c_ai:
    with st.container(border=True):
        st.markdown("### 🤖 AI Prediction")
        st.caption("Machine Learning (Probabilistic)")
        st.markdown("<br>", unsafe_allow_html=True)
        
        if ai_error:
            st.warning(ai_error)
        else:
            if ai_result:
                st.markdown('<div style="text-align:center"><span class="badge-dead">PREDICTED DEADLOCK</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center"><span class="badge-safe">PREDICTED SAFE</span></div>', unsafe_allow_html=True)
            
            st.markdown(f"**Confidence:** `{ai_proba*100:.2f}%`")
            st.progress(ai_proba)