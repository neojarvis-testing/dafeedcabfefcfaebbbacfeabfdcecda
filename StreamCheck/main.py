# kafka_producer.py

from kafka import KafkaProducer
import pandas as pd
import json
import time
import os

# Set CSV path
csv_path = "data.csv"

# Check if file exists
if not os.path.exists(csv_path):
    print(f"❌ File not found: {csv_path}")
    exit(1)

# Load the CSV
df = pd.read_csv(csv_path, on_bad_lines='skip')

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stream each row
for _, row in df.iterrows():
    data = row.to_dict()
    print("📤 Sending:", data)
    producer.send("noisy-topic", value=data)
    time.sleep(0.3)  # Simulate real-time streaming

producer.flush()
print("✅ Finished streaming CSV rows to Kafka.")
