from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

branches = ['Chennai', 'Bangalore', 'Hyderabad']

while True:
    txn = {
        "branch": random.choice(branches),
        "amount": random.randint(1000, 100000),
        "type": random.choice(["debit", "credit"])
    }
    producer.send("transactions", txn)
    print("Sent:", txn)
    time.sleep(2)
