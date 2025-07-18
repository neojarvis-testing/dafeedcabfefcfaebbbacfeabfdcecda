import streamlit as st
import sqlite3
import pandas as pd
import time
from genai.genai_explainer import get_risk_explanation

DB_PATH = "db/genai_fraud.db"

st.set_page_config(page_title="💸 Fraud Risk Dashboard", layout="wide")
st.title("🛡️ GenAI-Powered Fraud Detection System")

tab1, tab2, tab3 = st.tabs([
    "📊 Transaction Monitor", 
    "🚩 Fraud Case Analyzer", 
    "📁 Explained Cases Log"
])

# Helper
def get_connection():
    return sqlite3.connect(DB_PATH)

# --------------------- Tab 1 ---------------------
with tab1:
    st.subheader("📡 Live Transaction Stream (Kafka + ML)")

    placeholder = st.empty()
    refresh_interval = 5  # seconds

    def load_latest_transactions():
        conn = get_connection()
        df = pd.read_sql_query("""
            SELECT t.*, r.is_risky, r.model_confidence
            FROM transactions t
            LEFT JOIN risk_predictions r ON t.txn_id = r.txn_id
            ORDER BY t.timestamp DESC
            LIMIT 20
        """, conn)
        conn.close()
        return df

    with placeholder.container():
        latest_df = load_latest_transactions()
        st.dataframe(latest_df, use_container_width=True)
        st.caption(f"⏱ Refreshed every {refresh_interval} seconds automatically")

    time.sleep(refresh_interval)
    st.experimental_rerun()

# --------------------- Tab 2 ---------------------
with tab2:
    st.subheader("🔍 Fraud Case Analyzer")

    conn = get_connection()
    fraud_txns = pd.read_sql_query("""
        SELECT t.*, r.model_confidence
        FROM transactions t
        JOIN risk_predictions r ON t.txn_id = r.txn_id
        WHERE r.is_risky = 1
        AND t.txn_id NOT IN (SELECT txn_id FROM genai_analysis)
    """, conn)
    conn.close()

    ids = fraud_txns["txn_id"].tolist()

    if not ids:
        st.info("🎉 No unexplained fraudulent transactions available!")
    else:
        selected_txn = st.selectbox("Select a fraudulent transaction ID:", ids)

        if selected_txn:
            txn = fraud_txns[fraud_txns["txn_id"] == selected_txn].iloc[0]
            st.json(txn.to_dict())

            if st.button("🧠 Get GenAI Explanation"):
                with st.spinner("Calling Gemini API..."):
                    reason, suggestion = get_risk_explanation(txn.to_dict())
                st.success("✅ Explanation received!")
                st.markdown(f"**📌 Reason:** {reason}")
                st.markdown(f"**🛡 Suggestion:** {suggestion}")

                save = st.radio("Save this explanation to DB?", ["Yes", "No"])
                if save == "Yes":
                    conn = get_connection()
                    conn.execute("""
                        INSERT INTO genai_analysis (txn_id, risk_reason, mitigation_suggestion)
                        VALUES (?, ?, ?)
                    """, (txn["txn_id"], reason, suggestion))
                    conn.commit()
                    conn.close()
                    st.success("✅ Saved to DB and removed from dropdown!")
                    st.experimental_rerun()
                elif save == "No":
                    st.warning("❌ Discarded. Transaction remains in dropdown.")

# --------------------- Tab 3 ---------------------
with tab3:
    st.subheader("📁 GenAI-Reviewed Fraud Logs")

    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT t.txn_id, t.timestamp, t.amount, t.source_account, t.dest_account,
               g.risk_reason, g.mitigation_suggestion
        FROM genai_analysis g
        JOIN transactions t ON g.txn_id = t.txn_id
        ORDER BY t.timestamp DESC
    """, conn)
    conn.close()

    if df.empty:
        st.info("🕵️‍♀️ No transactions explained yet. Go to Tab 2 to analyze some!")
    else:
        st.dataframe(df, use_container_width=True)
