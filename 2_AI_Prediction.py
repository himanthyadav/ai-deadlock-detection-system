import streamlit as st
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix

# -----------------------------------------------------------------------------
# 1. PAGE CONFIG & THEME
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="AI Prediction",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
        html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
        
        div.stButton > button {
            background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
            color: white;
            border: none;
            padding: 0.75rem 1rem;
            font-weight: 600;
            border-radius: 0.5rem;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🤖 AI-Based Deadlock Prediction")
st.write("""
    This page uses **simulated data** and the **classical deadlock detection algorithm**
    to train a Machine Learning model that predicts whether a given state will
    lead to a deadlock or not.
""")

# -------- DEADLOCK LOGIC (Hidden) --------
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

# -------- RANDOM STATE GENERATION --------
def generate_random_state(n_proc=3, n_res=3):
    total = np.random.randint(3, 10, size=n_res)
    alloc = np.zeros((n_proc, n_res), dtype=int)
    for j in range(n_res):
        remaining = total[j]
        for i in range(n_proc):
            if i == n_proc - 1:
                a = np.random.randint(0, remaining + 1)
            else:
                a = np.random.randint(0, remaining + 1)
                remaining -= a
            alloc[i, j] = a
    req = np.zeros((n_proc, n_res), dtype=int)
    max_additional = total - alloc.sum(axis=0)
    for i in range(n_proc):
        for j in range(n_res):
            upper = max_additional[j] + alloc[i, j]
            req[i, j] = np.random.randint(0, upper + 1)
    label = int(detect_deadlock(total, alloc, req))
    return total, alloc, req, label

def build_dataset(n_samples=200, n_proc=3, n_res=3):
    X = []
    y = []
    for _ in range(n_samples):
        total, alloc, req, label = generate_random_state(n_proc, n_res)
        feat = np.concatenate([total.flatten(), alloc.flatten(), req.flatten()])
        X.append(feat)
        y.append(label)
    return np.array(X), np.array(y)

# -------- UI SECTIONS --------

# 1. Training Section
with st.container(border=True):
    st.subheader("1️⃣ Generate Training Data")
    n_samples = st.slider("Number of training examples", 50, 1000, 300, 50)

    if st.button("Generate Data & Train AI Model"):
        with st.spinner("Generating synthetic data and training Random Forest..."):
            X, y = build_dataset(n_samples=n_samples, n_proc=3, n_res=3)
            st.session_state["feature_dim"] = X.shape[1]

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            st.session_state["deadlock_model"] = model
            
            y_pred = model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            cm = confusion_matrix(y_test, y_pred)

        st.success("✅ Model trained successfully!")
        
        c1, c2 = st.columns(2)
        c1.metric("Test Accuracy", f"{acc*100:.2f}%")
        c2.metric("Dataset Size", len(X))
        
        st.caption("Confusion Matrix (Truth vs Prediction)")
        st.dataframe(pd.DataFrame(cm, index=["Safe", "Deadlock"], columns=["Pred Safe", "Pred Deadlock"]), use_container_width=True)

st.markdown("---")

# 2. Prediction Section
with st.container(border=True):
    st.subheader("2️⃣ Predict on Latest Simulation")
    
    if "deadlock_model" not in st.session_state:
        st.info("ℹ️ Please train the model in step 1 first.")
    elif "last_state" not in st.session_state:
        st.warning("No simulation data found. Please run the **Deadlock Simulation** first.")
    else:
        model = st.session_state["deadlock_model"]
        feat_dim = st.session_state.get("feature_dim", None)
        last = st.session_state["last_state"]
        
        # Prepare features
        total = np.array(last["total"])
        alloc = np.array(last["alloc"])
        req = np.array(last["req"])
        features = np.concatenate([total.flatten(), alloc.flatten(), req.flatten()]).reshape(1, -1)

        if feat_dim is not None and features.shape[1] != feat_dim:
            st.error("Dimension mismatch! The model was trained on a different P/R size. Please retrain.")
        else:
            pred = int(model.predict(features)[0])
            proba = model.predict_proba(features)[0][1]

            if pred == 1:
                st.error(f"⚠️ AI Prediction: **DEADLOCK LIKELY** ({proba*100:.1f}%)")
            else:
                st.success(f"✅ AI Prediction: **SAFE STATE** ({100-proba*100:.1f}%)")