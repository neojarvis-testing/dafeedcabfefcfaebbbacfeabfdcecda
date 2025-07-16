from kafka import KafkaProducer
import json
import random
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'sensor-readings'

# Simulate temperature sensor data
for _ in range(10):
    reading = {
        "sensor": "temp",
        "value": round(random.uniform(25.0, 35.0), 1)
    }
    producer.send(topic, value=reading)
    print(f"Produced: {reading}")
    time.sleep(1)

producer.flush()
producer.close()
