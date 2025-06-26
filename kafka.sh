#!/bin/bash
echo "🔍 Checking Kafka..."

# Start Zookeeper and Kafka
# # Start Zookeeper in background
# nohup /opt/kafka/bin/zookeeper-server-start.sh config/zookeeper.properties > zookeeper.log 2>&1 &

# # Start Kafka broker in background
# nohup /opt/kafka/bin/kafka-server-start.sh config/server.properties > kafka.log 2>&1 &

# Create a test topic
/opt/kafka/bin/kafka-topics.sh --create --topic test-topic --bootstrap-server 0.0.0.0:9092 --partitions 1 --replication-factor 1 \
  || echo "⚠️ Topic might already exist"

# List topics
/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server 0.0.0.0:9092

# Web UI
echo "[ℹ️] Kafka has no default Web UI. You can use Kafka Manager if needed."
