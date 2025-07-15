from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'logs',
    bootstrap_servers='localhost:9092',
    group_id='log_processors',  # same group ID
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest'
)

print("Consumer 2 started")

for msg in consumer:
    print("Consumer 2 got:", msg.value)
