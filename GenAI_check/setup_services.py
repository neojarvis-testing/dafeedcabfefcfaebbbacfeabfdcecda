import subprocess
import time

def setup_services():
    kafka_bin = "/opt/kafka/bin"
    kafka_conf = "/opt/kafka/config"
    spark_bin = "/opt/spark/bin"

    subprocess.Popen([f"{kafka_bin}/zookeeper-server-start.sh", f"{kafka_conf}/zookeeper.properties"])
    print("🦓 Zookeeper started")
    time.sleep(10)

    subprocess.Popen([f"{kafka_bin}/kafka-server-start.sh", f"{kafka_conf}/server.properties"])
    print("🦒 Kafka broker started")
    time.sleep(10)

    subprocess.run([
        f"{kafka_bin}/kafka-topics.sh", "--create", "--topic", "transactions",
        "--bootstrap-server", "localhost:9092", "--partitions", "1", "--replication-factor", "1"
    ], stderr=subprocess.DEVNULL)
    print("📌 Kafka topic created or already exists")

    subprocess.Popen([
        f"{spark_bin}/spark-submit",
        "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1",
        "spark_streaming/consumer.py"
    ])
    print("⚡ Spark consumer launched")
    time.sleep(5)

    subprocess.Popen(["python3", "kafka_producer/producer.py"])
    print("🚀 Kafka producer launched")

# ✅ Only run if executed directly
if __name__ == "__main__":
    setup_services()
