from kafka import KafkaProducer
import json
import time
import requests

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
topic = 'sensor-readings'
API_ENDPOINT = "https://mocki.io/v1/f4b4a676-2bcd-4c5c-84e0-55cd118e4a5e"

while True:
    try:
        response = requests.get(API_ENDPOINT)
        data = response.json()
        producer.send(topic, value=data)
        print(f"Produced: {data}")
        time.sleep(5)  # Polling interval
    except Exception as e:
        print("Error fetching sensor data:", e)
        time.sleep(10)

producer.flush()
producer.close()



