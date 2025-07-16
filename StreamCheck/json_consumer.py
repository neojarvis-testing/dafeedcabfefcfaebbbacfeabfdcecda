from kafka import KafkaConsumer
import json

# Create a Kafka consumer with JSON deserializer
consumer = KafkaConsumer(
    'user-events-json',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='json-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Waiting for JSON events...")

for message in consumer:
    event = message.value
    action = event.get("action", "unknown")
    page = event.get("page", "unknown")
    print(f"User {action}ed on {page}")
