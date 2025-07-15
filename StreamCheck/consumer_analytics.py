from kafka import KafkaConsumer
import json
import os

# Subscribe to all 3 topics
topics = ["ecom-transactions", "ecom-inventory", "ecom-pageviews"]

consumer = KafkaConsumer(
    *topics,
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='ecom-analytics-group'
)

print("📡 Listening to all e-commerce topics...")

try:
    for message in consumer:
        topic = message.topic
        data = message.value
        print(f"[{topic}] {data}")
        json.dump(data, file_handles[topic])
        file_handles[topic].write("\n")

except KeyboardInterrupt:
    print("🛑 Consumer stopped manually.")
