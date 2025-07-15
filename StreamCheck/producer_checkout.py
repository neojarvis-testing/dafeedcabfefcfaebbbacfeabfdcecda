from kafka import KafkaProducer
import json
import time

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample transaction events
transactions = [
    {"order_id": "T1001", "user_id": "U001", "amount": 1299.00, "status": "success"},
    {"order_id": "T1002", "user_id": "U002", "amount": 349.00, "status": "failed"},
    {"order_id": "T1003", "user_id": "U001", "amount": 2499.00, "status": "success"},
    {"order_id": "T1004", "user_id": "U003", "amount": 799.00, "status": "success"},
    {"order_id": "T1005", "user_id": "U004", "amount": 499.00, "status": "success"}
]

topic = "ecom-transactions"

for txn in transactions:
    print(f"Sending transaction: {txn}")
    producer.send(topic, value=txn)
    time.sleep(1)

producer.flush()
print("All transactions sent.")
