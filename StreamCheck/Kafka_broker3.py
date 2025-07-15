from kafka import KafkaProducer
import json
import time
import random

# Simulate broker behavior using a multi-partition topic on a single broker
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode()
)

for i in range(10):
    user_id = random.randint(1, 3)  # simulate 3 users
    order = {
        "order_id": 1000 + i,
        "user_id": user_id,
        "amount": round(random.uniform(50, 500), 2)
    }

    # Partitioning based on user_id
    producer.send("order-events", key=user_id, value=order)
    print(f"Sent to simulated partition for user_id {user_id}: {order}")
    time.sleep(1)

producer.flush()
