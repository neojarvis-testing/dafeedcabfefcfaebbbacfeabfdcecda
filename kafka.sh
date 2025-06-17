#!/bin/bash
echo "🔍 Checking Kafka..."

# Create a test topic
kafka-topics.sh --create --topic test-topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1 \
  || echo "⚠️ Topic might already exist"

# List topics
kafka-topics.sh --list --bootstrap-server localhost:9092

# Web UI
echo "[ℹ️] Kafka has no default Web UI. You can use Kafka Manager if needed."
