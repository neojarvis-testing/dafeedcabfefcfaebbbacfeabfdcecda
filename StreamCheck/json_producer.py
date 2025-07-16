from kafka import KafkaProducer
import json
import time

# Create a Kafka producer with JSON serializer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'user-events-json'

events = [
    {"action": "click", "page": "/home"},
    {"action": "scroll", "page": "/products"},
    {"action": "click", "page": "/cart"},
]

for event in events:
    producer.send(topic, value=event)
    print(f"Produced: {event}")
    time.sleep(1)

producer.flush()
producer.close()
