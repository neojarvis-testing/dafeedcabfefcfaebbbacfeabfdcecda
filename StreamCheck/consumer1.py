from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'logs',
    bootstrap_servers='localhost:9092',
    group_id='log_processors',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

print("Consumer 1 started")

for msg in consumer:
    print("Consumer 1 got:", msg.value)
