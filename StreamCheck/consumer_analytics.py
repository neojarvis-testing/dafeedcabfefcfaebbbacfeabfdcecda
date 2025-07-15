from kafka import KafkaConsumer
import json
import os

# Create output folder
os.makedirs("logs_output", exist_ok=True)

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

# Mapping topic to output file
topic_to_file = {
    "ecom-transactions": "logs_output/transactions.jsonl",
    "ecom-inventory": "logs_output/inventory.jsonl",
    "ecom-pageviews": "logs_output/pageviews.jsonl"
}

print("📡 Listening to all e-commerce topics...")

file_handles = {
    topic: open(path, "a", encoding="utf-8")
    for topic, path in topic_to_file.items()
}

try:
    for message in consumer:
        topic = message.topic
        data = message.value
        print(f"[{topic}] {data}")
        json.dump(data, file_handles[topic])
        file_handles[topic].write("\n")

except KeyboardInterrupt:
    print("🛑 Consumer stopped manually.")
finally:
    for fh in file_handles.values():
        fh.close()
