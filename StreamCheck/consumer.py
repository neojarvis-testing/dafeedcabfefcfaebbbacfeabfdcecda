from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'simple-messages',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='demo-consumer-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

print("Waiting for messages...")
for message in consumer:
    print(f"Consumed: {message.value}")

