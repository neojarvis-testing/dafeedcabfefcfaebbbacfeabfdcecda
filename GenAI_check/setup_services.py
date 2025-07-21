import subprocess
import time
import signal

def setup_services():
    kafka_bin = "/opt/kafka/bin"
    kafka_conf = "/opt/kafka/config"
    spark_bin = "/opt/spark/bin"

    processes = []

    try:
        # Start Zookeeper
        zk = subprocess.Popen([
            f"{kafka_bin}/zookeeper-server-start.sh",
            f"{kafka_conf}/zookeeper.properties"
        ])
        processes.append(zk)
        print("🦓 Zookeeper started")
        time.sleep(10)

        # Start Kafka Server
        kafka = subprocess.Popen([
            f"{kafka_bin}/kafka-server-start.sh",
            f"{kafka_conf}/server.properties"
        ])
        processes.append(kafka)
        print("🦒 Kafka broker started")
        time.sleep(10)

        # Create Kafka Topic
        subprocess.run([
            f"{kafka_bin}/kafka-topics.sh", "--create", "--topic", "transactions",
            "--bootstrap-server", "localhost:9092", "--partitions", "1", "--replication-factor", "1"
        ], stderr=subprocess.DEVNULL)
        print("📌 Kafka topic created or already exists")

        # Start Spark Consumer
        consumer = subprocess.Popen([
            f"{spark_bin}/spark-submit",
            "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
            "spark_streaming/consumer.py"
        ])
        processes.append(consumer)
        print("⚡ Spark consumer launched")
        time.sleep(5)

        # Start Kafka Producer
        producer = subprocess.Popen(["python3", "kafka_producer/producer.py"])
        processes.append(producer)
        print("🚀 Kafka producer launched")

        print("\n✅ All services running. Press Ctrl+C to stop them...\n")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Ctrl+C detected. Terminating all services...")
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=10)
            except Exception as e:
                print(f"⚠️ Error terminating process: {e}")
        print("✅ All services stopped.")

if __name__ == "__main__":
    setup_services()
