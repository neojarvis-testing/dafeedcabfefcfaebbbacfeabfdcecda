from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode()
)

for i in range(10):
    user_id = random.randint(1, 3)
    order = {
        "order_id": 1000 + i,
        "user_id": user_id,
        "amount": round(random.uniform(50, 500), 2)
    }

    # Send the message and get metadata about the result
    future = producer.send("order-events", key=user_id, value=order)
    record_metadata = future.get(timeout=10)  # Block until ack

    print(f"Sent order: {order} → Partition: {record_metadata.partition}")

    time.sleep(1)

producer.flush()

