from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: v.encode('utf-8')
)

topic = 'simple-messages'

for i in range(5):
    message = f'Hello Kafka {i}'
    producer.send(topic, value=message)
    print(f'Produced: {message}')
    time.sleep(1)

producer.flush()
producer.close()
