from kafka import KafkaProducer
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

topic = 'sensor-readings'

for reading in sensor_data_stream:
    producer.send(topic, value=reading)
    print(f"Produced: {reading}")
    time.sleep(1)  # Simulating real-time arrival

producer.flush()
producer.close()
