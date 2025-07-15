#!/bin/bash

echo "🟡 Starting Zookeeper and Kafka..."

# Start Zookeeper
nohup /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties > zookeeper.log 2>&1 &

# Wait for Zookeeper to be ready
sleep 5

# Start Kafka
nohup /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties > kafka.log 2>&1 &
