from kafka import KafkaConsumer
import json
import os

# Create output directory if it doesn't exist
os.makedirs("logs_output", exist_ok=True)

# Initialize Kafka consumer
consumer = KafkaConsumer(
    'user-activity',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='activity-filter-group'
)

suspicious_keywords = ["delete_account", "password_change"]
output_file = "logs_output/filtered.jsonl"

print("Starting consumer...")

with open(output_file, "a", encoding="utf-8") as outfile:
    for message in consumer:
        data = message.value
        if data["action"] in suspicious_keywords:
            print(f"Suspicious action detected: {data}")
            outfile.write(json.dumps(data) + "\n")
