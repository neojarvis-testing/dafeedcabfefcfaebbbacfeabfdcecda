from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    key_serializer=lambda k: str(k).encode()
)

event_types = ["click", "order"]

for i in range(10):
    user_id = random.randint(1, 3)
    event_type = random.choice(event_types)

    event = {
        "user_id": user_id,
        "event_type": event_type,
        "timestamp": time.time(),
        "details": f"Simulated {event_type} event"
    }

    topic = "click-events" if event_type == "click" else "order-events"
    future = producer.send(topic, key=user_id, value=event)
    metadata = future.get(timeout=10)

    print(f"Sent {event_type} event for user {user_id} to topic `{topic}` → Partition {metadata.partition}")

    time.sleep(1)

producer.flush()

