import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

# Initialize Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Sample options
txn_types = ['UPI', 'NEFT', 'MANDATE', 'CHEQUE']
accounts = ['AC001', 'AC002', 'AC003', 'AC004', 'AC005']
devices = ['mobile', 'web', 'tablet']
statuses = ['Success', 'Failed', 'Pending']

def generate_transaction():
    source = random.choice(accounts)
    destination = random.choice([acc for acc in accounts if acc != source])
    return {
        "txn_id": f"TX{random.randint(100000, 999999)}",
        "timestamp": datetime.now().isoformat(),
        "txn_type": random.choice(txn_types),
        "amount": round(random.uniform(1000, 1000000), 2),
        "source_account": source,
        "dest_account": destination,
        "status": random.choices(statuses, weights=[0.85, 0.1, 0.05])[0],
        "ip_address": f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}",
        "device_id": random.choice(devices)
    }

if __name__ == "__main__":
    print("📡 Kafka Producer started. Sending transactions to topic: 'transactions'")
    try:
        while True:
            txn = generate_transaction()
            producer.send("transactions", value=txn)
            print("📤 Sent:", txn)
            time.sleep(1.5)  # Simulate ~1.5 sec interval between transactions
    except KeyboardInterrupt:
        print("🛑 Stopped by user.")
    finally:
        producer.flush()
        producer.close()
