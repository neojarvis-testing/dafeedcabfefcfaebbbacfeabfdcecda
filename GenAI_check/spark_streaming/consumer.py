from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType
import pandas as pd
import joblib
import sqlite3

# Load trained ML model & encoders
model = joblib.load("models/fraud_model.pkl")
encoders = joblib.load("models/label_encoders.pkl")
target_encoder = joblib.load("models/target_encoder.pkl")

# SQLite setup
def save_to_db(record, prediction):
    conn = sqlite3.connect("db/genai_fraud.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (
            txn_id, timestamp, txn_type, amount, source_account,
            dest_account, status, ip_address, device_id, is_fraud
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        record["txn_id"], record["timestamp"], record["txn_type"], record["amount"],
        record["source_account"], record["dest_account"], record["status"],
        record["ip_address"], record["device_id"], prediction
    ))
    conn.commit()
    conn.close()

# Define schema
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

# Spark session
spark = SparkSession.builder \
    .appName("FraudDetectionConsumer") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read Kafka stream
df_kafka_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

# Parse Kafka JSON
df_parsed = df_kafka_raw.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# Define ML processing function
def process_row(row):
    row_dict = row.asDict()
    df = pd.DataFrame([row_dict])

    # Encode categorical features
    for col_name in encoders:
        df[col_name] = encoders[col_name].transform(df[col_name])

    X = df[['txn_type', 'amount', 'source_account', 'dest_account', 'status', 'ip_address', 'device_id']]
    prediction = model.predict(X)[0]
    decoded_label = target_encoder.inverse_transform([prediction])[0]

    save_to_db(row_dict, decoded_label)

# Stream handler
def foreach_batch(df, epoch_id):
    df.persist()
    df.foreach(process_row)
    df.unpersist()

# Start stream
query = df_parsed.writeStream \
    .foreachBatch(foreach_batch) \
    .start()

query.awaitTermination()
