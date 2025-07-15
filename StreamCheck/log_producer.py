from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

log_types = ['app_log', 'user_log']

for i in range(10):
    event = {
        "log_type": random.choice(log_types),
        "timestamp": time.time(),
        "message": f"Log message #{i}"
    }
    producer.send("logs", value=event)
    print("Produced:", event)
    time.sleep(0.5)

producer.flush()
