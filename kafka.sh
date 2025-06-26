#!/bin/bash
echo "🔍 Checking Kafka..."

# Start Zookeeper and Kafka
# Start Zookeeper in background
nohup bin/zookeeper-server-start.sh config/zookeeper.properties > zookeeper.log 2>&1 &

# Start Kafka broker in background
nohup bin/kafka-server-start.sh config/server.properties > kafka.log 2>&1 &

# Create a test topic
kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 \
  || echo "⚠️ Topic might already exist"

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Web UI
echo "[ℹ️] Kafka has no default Web UI. You can use Kafka Manager if needed."
