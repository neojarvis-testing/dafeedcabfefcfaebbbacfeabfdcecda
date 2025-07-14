import time
from kafka import KafkaProducer
import pandas as pd
import json

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda m: json.dumps(m).encode("utf-8")
)

csv_path = "data.csv"  # or noisy_events.csv
df = pd.read_csv(csv_path)

for _, row in df.iterrows():
    record = row.to_dict()
    producer.send("noisy-topic", value=record)
    print("📤 Streaming:", record)
    time.sleep(2)  # delay between messages
