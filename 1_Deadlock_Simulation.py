import streamlit as st
import pandas as pd
import numpy as np
import time

st.set_page_config(
    page_title="Deadlock Simulation",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .result-box-safe {
        background-color: #ecfdf5;
        border: 2px solid #10b981;
        padding: 20px;
        border-radius: 10px;
        color: #064e3b;
        text-align: center;
        margin-top: 20px;
    }
    .result-box-dead {
        background-color: #fef2f2;
        border: 2px solid #ef4444;
        padding: 20px;
        border-radius: 10px;
        color: #7f1d1d;
        text-align: center;
        margin-top: 20px;
    }
    div.stButton > button {
        background: linear-gradient(90deg, #2563eb 0%, #4f46e5 100%);
        color: white;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: 600;
        border-radius: 0.5rem;
        width: 100%;
        transition: all 0.2s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 10px rgba(37, 99, 235, 0.2);
    }
</style>
""", unsafe_allow_html=True)


st.title("🛡️ Deadlock Simulation")

with st.container(border=True):
    st.subheader("⚙️ System Configuration")

    col_mode, col_p, col_r = st.columns([1.5, 1, 1])
    with col_mode:
        mode = st.radio(
            "Resource Type",
            ["Single Instance", "Multiple Instance"],
            horizontal=True
        )
    with col_p:
        num_processes = st.number_input(
            "Number of Processes (P)",
            min_value=2, max_value=10, value=3, step=1
        )
    with col_r:
        num_resources = st.number_input(
            "Number of Resources (R)",
            min_value=1, max_value=10, value=3, step=1
        )

st.markdown("<br>", unsafe_allow_html=True)


with st.container(border=True):
    st.subheader("1️⃣ Total Resource Capacity")
    st.caption("Maximum number of instances available for each resource type.")

    total_resources = []
    total_cols = st.columns(num_resources)
    for j, col in enumerate(total_cols):
        with col:
            val = st.number_input(
                f"R{j} (Total Capacity)",
                min_value=1,
                max_value=100,
                value=7 if j == 0 else 5,   # some default
                step=1,
                key=f"total_r{j}"
            )
            total_resources.append(val)

total = np.array(total_resources, dtype=int)

st.markdown("<br>", unsafe_allow_html=True)


st.subheader("2️⃣ Current System State")

col_alloc, col_req = st.columns(2)


with col_alloc:
    st.info("🟦 Allocation Matrix (Resources currently held)")
    default_alloc = pd.DataFrame(
        0,
        index=[f"P{i}" for i in range(num_processes)],
        columns=[f"R{j}" for j in range(num_resources)]
    )
    alloc_df = st.data_editor(
        default_alloc,
        num_rows="fixed",
        use_container_width=True,
        key="alloc_editor"
    )


with col_req:
    st.warning("🟨 Request Matrix (Remaining resources needed to finish)")
    default_req = pd.DataFrame(
        0,
        index=[f"P{i}" for i in range(num_processes)],
        columns=[f"R{j}" for j in range(num_resources)]
    )
    req_df = st.data_editor(
        default_req,
        num_rows="fixed",
        use_container_width=True,
        key="req_editor"
    )

st.markdown("---")

st.subheader("3️⃣ Automatically Computed Available Resources")

alloc = alloc_df.to_numpy(dtype=int)
req = req_df.to_numpy(dtype=int)

allocated_sum = alloc.sum(axis=0)
available = total - allocated_sum

# Display metrics
avail_cols = st.columns(num_resources)
for j, col in enumerate(avail_cols):
    with col:
        if available[j] < 0:
            col.metric(f"R{j}", int(available[j]), delta="Invalid (Negative!)")
        else:
            col.metric(f"R{j}", int(available[j]))

if np.any(available < 0):
    st.error("🚨 Allocated resources exceed Total Capacity! Please correct values.")
    st.stop()

st.markdown("---")


st.subheader("4️⃣ Simulation Analysis")

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    run_btn = st.button("🚀 DETECT DEADLOCK", type="primary")

def bankers_deadlock(total_vec, alloc_mat, req_mat):
    """
    total_vec : (m,) total capacity of each resource
    alloc_mat : (n,m) allocation
    req_mat   : (n,m) remaining need / request
    returns (is_deadlock, safe_sequence, deadlocked_processes, final_available)
    """
    total_vec = np.array(total_vec, dtype=int)
    alloc_mat = np.array(alloc_mat, dtype=int)
    req_mat = np.array(req_mat, dtype=int)

    n, m = alloc_mat.shape
    work = total_vec - alloc_mat.sum(axis=0)      
    finish = np.array([False] * n)
    safe_seq = []

    changed = True
    while changed:
        changed = False
        for i in range(n):
            if not finish[i] and np.all(req_mat[i] <= work):
                # this process can finish
                work = work + alloc_mat[i]
                finish[i] = True
                safe_seq.append(f"P{i}")
                changed = True

    deadlocked = [f"P{i}" for i in range(n) if not finish[i]]
    is_deadlock = len(deadlocked) > 0
    return is_deadlock, safe_seq, deadlocked, work

if run_btn:
    
    st.session_state["last_state"] = {
        "total": total.tolist(),
        "alloc": alloc.tolist(),
        "req": req.tolist(),
    }

    with st.status("Running Banker's Algorithm...", expanded=True) as status:
        time.sleep(0.4)

        is_dead, safe_seq, deadlocked, final_avail = bankers_deadlock(total, alloc, req)

        status.update(label="Analysis Complete", state="complete", expanded=False)

    
    if not is_dead:
        label_mode = "Single Instance" if mode == "Single Instance" else "Multiple Instance"
        st.markdown(f"""
        <div class="result-box-safe">
            <h2>✅ SAFE STATE ({label_mode})</h2>
            <h4>Safe Sequence: {" → ".join(safe_seq) if safe_seq else "None (all zero requests)"}</h4>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.caption("Final Available Resources after completing all processes:")
        cols_metric = st.columns(len(final_avail))
        for j, val in enumerate(final_avail):
            cols_metric[j].metric(f"R{j}", int(val), delta="Freed")
    else:
        st.markdown(f"""
        <div class="result-box-dead">
            <h2>💀 DEADLOCK DETECTED</h2>
            <p>Type: {"Single Instance" if mode == "Single Instance" else "Multiple Instance"}</p>
            <p>Blocked Processes: {", ".join(deadlocked)}</p>
        </div>
        """, unsafe_allow_html=True)



