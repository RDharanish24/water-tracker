import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
# Update this URL to match your FastAPI server address
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Water Tracker", page_icon="💧", layout="wide")

# --- SESSION STATE ---
if "user_id" not in st.session_state:
    st.session_state.user_id = "user_1"

# --- UI HEADER ---
st.title("💧 AI Hydration Companion")
st.markdown("---")

# --- SIDEBAR: LOGGING ---
with st.sidebar:
    st.header("Log Intake")
    amount = st.number_input("Amount (ml)", min_value=0, step=50, value=250)
    
    if st.button("Add Water 🥤", use_container_width=True):
        payload = {"user_id": st.session_state.user_id, "intake_ml": amount}
        try:
            response = requests.post(f"{BACKEND_URL}/log-intake", json=payload)
            if response.status_code == 200:
                st.success(f"Logged {amount}ml successfully!")
                st.balloons()
            else:
                st.error("Failed to log intake.")
        except Exception as e:
            st.error(f"Connection Error: {e}")

# --- MAIN DASHBOARD ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Today's Progress")
    try:
        # Fetch history from backend
        resp = requests.get(f"{BACKEND_URL}/history/{st.session_state.user_id}")
        if resp.status_code == 200:
            data = resp.json()
            history = data.get("history", [])
            
            # Calculate total for today
            today_str = datetime.now().strftime("%Y-%m-%d")
            total_today = sum(item['ml'] for item in history if item['date'] == today_str)
            
            # Progress Visuals
            goal = 2500
            progress = min(total_today / goal, 1.0)
            
            c1, c2 = st.columns(2)
            c1.metric("Total Drunk", f"{total_today} ml")
            c2.metric("Goal", f"{goal} ml", f"{total_today - goal} ml")
            
            st.progress(progress)
            st.write(f"**{int(progress * 100)}%** of your daily goal reached.")
            
            # AI Insight Section
            st.markdown("### 🤖 AI Hydration Analysis")
            if st.button("Get AI Feedback", type="primary"):
                # We reuse the log-intake endpoint with 0 to trigger the latest analysis
                # Or better, if you have an analysis endpoint, call that.
                # Assuming the last analysis is part of the log-intake response:
                log_resp = requests.post(f"{BACKEND_URL}/log-intake", 
                                       json={"user_id": st.session_state.user_id, "intake_ml": 0})
                analysis = log_resp.json().get("analysis", "No data yet.")
                st.info(analysis)
        else:
            st.warning("Could not retrieve history.")
    except:
        st.error("Is your backend server running?")

with col2:
    st.subheader("Recent Logs")
    if 'history' in locals() and history:
        df = pd.DataFrame(history)
        if not df.empty:
            df = df.rename(columns={"ml": "Amount (ml)", "date": "Date"})
            st.dataframe(df.sort_index(ascending=False), use_container_width=True, hide_index=True)
    else:
        st.write("No logs recorded yet.")

# --- FOOTER ---
st.markdown("---")
st.caption("Powered by Gemini 3 Flash Lite & FastAPI")