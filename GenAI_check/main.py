import streamlit as st
import sqlite3
import pandas as pd
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

    if st.button("🔁 Refresh Transactions"):
        conn = get_connection()
        df = pd.read_sql_query("""
            SELECT t.*, r.is_risky, r.model_confidence
            FROM transactions t
            LEFT JOIN risk_predictions r ON t.txn_id = r.txn_id
            ORDER BY t.timestamp DESC
            LIMIT 20
        """, conn)
        conn.close()
        st.dataframe(df, use_container_width=True)
        st.success("🔄 Refreshed latest transactions!")

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

    txn_ids = fraud_txns["txn_id"].tolist()

    if not txn_ids:
        st.info("🎉 No unexplained fraudulent transactions available!")
    else:
        options = ["Select a transaction_id"] + txn_ids
        selected_txn = st.selectbox("Choose a fraudulent transaction:", options)

        if selected_txn != "Select a transaction_id":
            txn = fraud_txns[fraud_txns["txn_id"] == selected_txn].iloc[0]
            st.markdown("### 🧾 Transaction Details")
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Transaction ID:** {txn['txn_id']}")
                st.write(f"**Type:** {txn['txn_type']}")
                st.write(f"**Status:** {txn['status']}")
                st.write(f"**Amount:** ₹{txn['amount']}")
            with col2:
                st.write(f"**Source Account:** {txn['source_account']}")
                st.write(f"**Destination Account:** {txn['dest_account']}")
                st.write(f"**IP Address:** {txn['ip_address']}")
                st.write(f"**Device ID:** {txn['device_id']}")

            if st.button("🧠 Get GenAI Explanation"):
                with st.spinner("Calling Gemini API..."):
                    reason, suggestion = get_risk_explanation(txn.to_dict())

                st.success("✅ Explanation received!")
                st.markdown(f"#### 📌 Reason:\n{reason}")
                st.markdown(f"#### 🛡 Suggestion:\n{suggestion}")

                save = st.radio("Save this explanation to DB?", ["Yes", "No"], index=None, horizontal=True)
                if save == "Yes":
                    conn = get_connection()
                    conn.execute("""
                        INSERT INTO genai_analysis (txn_id, risk_reason, mitigation_suggestion)
                        VALUES (?, ?, ?)
                    """, (txn["txn_id"], reason, suggestion))
                    conn.commit()
                    conn.close()
                    st.success("✅ Saved to DB! Please refresh tab to remove it from dropdown.")

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
