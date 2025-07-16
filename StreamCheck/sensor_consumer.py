from kafka import KafkaConsumer
import json
consumer = KafkaConsumer(
    'sensor-readings',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='sensor-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)
print("Monitoring sensor values...")
for message in consumer:
    data = message.value
    sensor = data.get("sensor")
    value = data.get("value")

    if sensor == "temp" and value > 30.0:
        print(f"ALERT: {value}°C from {sensor} sensor")


