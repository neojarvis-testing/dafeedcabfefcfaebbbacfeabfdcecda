from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample inventory events
inventory_updates = [
    {"product_id": "P1001", "stock_change": -2, "location": "Warehouse-A"},
    {"product_id": "P1002", "stock_change": 10, "location": "Warehouse-B"},
    {"product_id": "P1003", "stock_change": -1, "location": "Warehouse-A"},
    {"product_id": "P1001", "stock_change": 20, "location": "Warehouse-C"},
    {"product_id": "P1004", "stock_change": -5, "location": "Warehouse-B"}
]

topic = "ecom-inventory"

for update in inventory_updates:
    print(f"Sending inventory update: {update}")
    producer.send(topic, value=update)
    time.sleep(1)

producer.flush()
print("All inventory updates sent.")
