#!/bin/bash
echo "🔍 Checking Kafka..."

# Start Zookeeper and Kafka
nohup $KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties > /var/log/zookeeper.log 2>&1 &
sleep 5
nohup $KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties > /var/log/kafka.log 2>&1 &

# Create a test topic
kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 \
  || echo "⚠️ Topic might already exist"

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Web UI
echo "[ℹ️] Kafka has no default Web UI. You can use Kafka Manager if needed."
