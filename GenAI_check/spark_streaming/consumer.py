from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType
import pandas as pd
import joblib
import sqlite3
import os

# -----------------------------
# Path setup (absolute-relative fix)
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, '../models/fraud_model.pkl')
ENCODERS_PATH = os.path.join(BASE_DIR, '../models/label_encoders.pkl')
TARGET_ENCODER_PATH = os.path.join(BASE_DIR, '../models/target_encoder.pkl')
DB_PATH = os.path.join(BASE_DIR, '../db/genai_fraud.db')

# -----------------------------
# Load trained ML model & encoders
# -----------------------------
model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODERS_PATH)
target_encoder = joblib.load(TARGET_ENCODER_PATH)

# -----------------------------
# Save to SQLite DB
# -----------------------------
def save_to_db(record, prediction):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 1: Insert raw transaction
    cursor.execute("""
        INSERT OR IGNORE INTO transactions (
            txn_id, timestamp, txn_type, amount, source_account,
            dest_account, status, ip_address, device_id
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["txn_id"], record["timestamp"], record["txn_type"], record["amount"],
        record["source_account"], record["dest_account"], record["status"],
        record["ip_address"], record["device_id"]
    ))

    # Step 2: Insert prediction (binary label: risky/fraud = 1, normal = 0)
    is_risky = 1 if prediction == "fraud" else 0

    cursor.execute("""
        INSERT OR REPLACE INTO risk_predictions (
            txn_id, is_risky, model_confidence
        ) VALUES (?, ?, ?)
    """, (
        record["txn_id"], is_risky, None  # Confidence can be added later if needed
    ))

    conn.commit()
    conn.close()

# -----------------------------
# Kafka schema
# -----------------------------
schema = StructType() \
    .add("txn_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("txn_type", StringType()) \
    .add("amount", DoubleType()) \
    .add("source_account", StringType()) \
    .add("dest_account", StringType()) \
    .add("status", StringType()) \
    .add("ip_address", StringType()) \
    .add("device_id", StringType())

# -----------------------------
# Spark session
# -----------------------------
spark = SparkSession.builder \
    .appName("FraudDetectionConsumer") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# -----------------------------
# Kafka stream
# -----------------------------
df_kafka_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

df_parsed = df_kafka_raw.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# -----------------------------
# Per-row processing
# -----------------------------
def process_row(row):
    row_dict = row.asDict()
    df = pd.DataFrame([row_dict])

    # Convert to string and handle unknowns
    for col_name, encoder in encoders.items():
        df[col_name] = df[col_name].astype(str)
        df[col_name] = df[col_name].apply(
            lambda val: val if val in encoder.classes_ else "unknown"
        )
        df[col_name] = encoder.transform(df[col_name])

    # Feature selection
    X = df[['txn_type', 'amount', 'source_account', 'dest_account', 'status', 'ip_address', 'device_id']]
    prediction = model.predict(X)[0]
    decoded_label = target_encoder.inverse_transform([prediction])[0]

    # Save to DB
    save_to_db(row_dict, decoded_label)

# -----------------------------
# Batch handler
# -----------------------------
def foreach_batch(df, epoch_id):
    df.persist()
    df.foreach(process_row)
    df.unpersist()

# -----------------------------
# Start streaming
# -----------------------------
query = df_parsed.writeStream \
    .foreachBatch(foreach_batch) \
    .start()

query.awaitTermination()
