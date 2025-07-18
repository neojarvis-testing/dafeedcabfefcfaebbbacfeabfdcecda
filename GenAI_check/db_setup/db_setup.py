import sqlite3
import os

# Create 'db' directory if it doesn't exist
os.makedirs("db", exist_ok=True)

# Connect to SQLite database (will create if it doesn't exist)
conn = sqlite3.connect("db/genai_fraud.db")
cursor = conn.cursor()

# Create table for raw transactions
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    txn_id TEXT PRIMARY KEY,
    timestamp TEXT,
    txn_type TEXT,
    amount REAL,
    source_account TEXT,
    dest_account TEXT,
    status TEXT,
    ip_address TEXT,
    device_id TEXT
)
""")

# Create table for ML risk predictions
cursor.execute("""
CREATE TABLE IF NOT EXISTS risk_predictions (
    txn_id TEXT PRIMARY KEY,
    is_risky INTEGER,
    model_confidence REAL,
    FOREIGN KEY (txn_id) REFERENCES transactions(txn_id)
)
""")

# Create table for GenAI explanations
cursor.execute("""
CREATE TABLE IF NOT EXISTS genai_analysis (
    txn_id TEXT PRIMARY KEY,
    risk_reason TEXT,
    mitigation_suggestion TEXT,
    FOREIGN KEY (txn_id) REFERENCES risk_predictions(txn_id)
)
""")

conn.commit()
conn.close()

print("✅ SQLite database setup complete. Tables created in 'db/genai_fraud.db'.")
