# kafka_producer.py

from kafka import KafkaProducer
import time

# Configure Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = 'tweets'

# Path to the tweet dataset
file_path = 'sample_tweets.txt'

# Stream each tweet line-by-line
with open(file_path, 'r', encoding='utf-8') as file:
    for line in file:
        tweet = line.strip()
        if tweet:
            producer.send(topic, value=tweet.encode('utf-8'))
            print(f"Sent: {tweet}")
            time.sleep(1.5)  # Simulate tweet interval

producer.flush()
producer.close()
