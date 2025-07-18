# genai/genai_trigger.py

import sqlite3
from genai_explainer import get_risk_explanation
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../db/genai_fraud.db")

def process_unexplained_frauds():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Fetch fraud txn_ids that do not exist in genai_analysis
    cursor.execute("""
        SELECT rp.txn_id
        FROM risk_predictions rp
        LEFT JOIN genai_analysis ga ON rp.txn_id = ga.txn_id
        WHERE rp.is_risky = 1 AND ga.txn_id IS NULL
    """)
    rows = cursor.fetchall()
    unexplained_ids = [row[0] for row in rows]

    if not unexplained_ids:
        print("✅ No unexplained risky transactions found.")
        return

    print(f"🔍 Found {len(unexplained_ids)} unexplained risky transactions.")

    for txn_id in unexplained_ids:
        # Get full transaction
        cursor.execute("SELECT * FROM transactions WHERE txn_id = ?", (txn_id,))
        txn_row = cursor.fetchone()
        col_names = [desc[0] for desc in cursor.description]
        txn_dict = dict(zip(col_names, txn_row))

        # Get GenAI explanation
        reason, mitigation = get_risk_explanation(txn_dict)

        # Save explanation
        cursor.execute("""
            INSERT INTO genai_analysis (txn_id, risk_reason, mitigation_suggestion)
            VALUES (?, ?, ?)
        """, (txn_id, reason, mitigation))
        print(f"✅ Explained txn_id {txn_id}")

    conn.commit()
    conn.close()
    print("📌 GenAI analysis updated in DB.")
