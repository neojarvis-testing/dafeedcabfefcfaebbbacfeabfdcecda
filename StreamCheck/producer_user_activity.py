from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample user actions to simulate (read from file or generate)
user_actions = [
    {"user_id": "U001", "action": "login", "timestamp": "2025-07-15T10:01:12"},
    {"user_id": "U002", "action": "delete_account", "timestamp": "2025-07-15T10:01:13"},
    {"user_id": "U003", "action": "view_product", "timestamp": "2025-07-15T10:01:14"},
    {"user_id": "U004", "action": "password_change", "timestamp": "2025-07-15T10:01:15"},
    {"user_id": "U005", "action": "logout", "timestamp": "2025-07-15T10:01:16"}
]

topic = "user-activity"

for action in user_actions:
    print(f"Sending: {action}")
    producer.send(topic, value=action)
    time.sleep(1)

producer.flush()
print("All events sent.")
