# kafka_consumer.py

import json
import os
import csv
from kafka import KafkaConsumer
from datetime import datetime

OUTPUT_FILE = "output/cleaned_events.csv"
ALLOWED_EVENTS = {"login", "logout", "purchase"}

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

def is_valid_record(record):
    try:
        # Check and clean event_type
        event = record.get("event_type")
        if not isinstance(event, str):
            return False
        record["event_type"] = event.strip().lower()

        # Check and clean value
        value = record["value"]
        if not str(value).strip().isdigit():
            return False
        record["value"] = int(value)

        # Check and parse timestamp
        ts = record["timestamp"]
        ts_cleaned = str(ts).strip()
        valid_formats = ["%Y-%m-%d %H:%M:%S", "%Y/%m/%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S"]
        parsed = None
        for fmt in valid_formats:
            try:
                parsed = datetime.strptime(ts_cleaned, fmt)
                break
            except:
                continue
        if not parsed:
            return False
        record["timestamp"] = parsed.strftime("%Y-%m-%d %H:%M:%S")

        # Basic check for user_id
        if not record["user_id"] or str(record["user_id"]).strip() == "":
            return False

        return True

    except Exception as e:
        print(f"❌ Invalid record: {record} → {e}")
        return False

def consume_and_clean():
    consumer = KafkaConsumer(
        "noisy-topic",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="earliest",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        consumer_timeout_ms=5000  # Exit after 5s if no more data
    )

    cleaned_data = []

    for message in consumer:
        record = message.value
        if is_valid_record(record):
            cleaned_data.append(record)

    if cleaned_data:
        with open(OUTPUT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["user_id", "event_type", "value", "timestamp"])
            writer.writeheader()
            writer.writerows(cleaned_data)
        print(f"✅ Saved {len(cleaned_data)} cleaned rows to {OUTPUT_FILE}")
    else:
        print("⚠️ No valid rows found.")

if __name__ == "__main__":
    consume_and_clean()
