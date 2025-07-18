# kafka_producer/producer.py

import json
import time
import random
from datetime import datetime
from kafka import KafkaProducer

TOPIC = "transactions"
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

ACCOUNTS = ["AC001", "AC002", "AC003", "AC004", "AC005"]
TXN_TYPES = ["NEFT", "UPI", "CHEQUE", "MANDATE"]
DEVICE_IDS = ["web", "mobile", "tablet"]
STATUSES = ["Success", "Pending", "Failed"]

def generate_transaction():
    is_risky = random.random() < 0.12  # ~12% are risky

    if is_risky:
        txn = {
            "txn_id": f"TX{random.randint(100000, 999999)}",
            "timestamp": datetime.utcnow().isoformat(),
            "txn_type": random.choice(["UPI", "CHEQUE"]),  # suspicious for big txn
            "amount": round(random.uniform(800000, 2000000), 2),
            "source_account": random.choice(ACCOUNTS),
            "dest_account": random.choice(ACCOUNTS),
            "status": random.choice(STATUSES),
            "ip_address": f"10.10.{random.randint(0, 255)}.{random.randint(1, 255)}",
            "device_id": random.choice(["mobile", "tablet"])  # mobile risk
        }
    else:
        txn = {
            "txn_id": f"TX{random.randint(100000, 999999)}",
            "timestamp": datetime.utcnow().isoformat(),
            "txn_type": random.choice(TXN_TYPES),
            "amount": round(random.uniform(1000, 500000), 2),
            "source_account": random.choice(ACCOUNTS),
            "dest_account": random.choice(ACCOUNTS),
            "status": random.choice(STATUSES),
            "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(1, 255)}",
            "device_id": random.choice(DEVICE_IDS)
        }
    return txn

print(f"📡 Kafka Producer started. Sending transactions to topic: '{TOPIC}'")

try:
    while True:
        txn = generate_transaction()
        producer.send(TOPIC, value=txn)
        print(f"📤 Sent: {txn}")
        time.sleep(2)
except KeyboardInterrupt:
    print("🛑 Stopped by user.")
