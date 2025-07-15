from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample page view events
page_views = [
    {"user_id": "U001", "page": "/home"},
    {"user_id": "U002", "page": "/products/P1001"},
    {"user_id": "U003", "page": "/cart"},
    {"user_id": "U004", "page": "/products/P1003"},
    {"user_id": "U001", "page": "/checkout"}
]

topic = "ecom-pageviews"

for event in page_views:
    print(f"Sending page view event: {event}")
    producer.send(topic, value=event)
    time.sleep(1)

producer.flush()
print("All page view events sent.")
