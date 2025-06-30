#!/bin/bash
 
echo "🔍 Verifying Big Data Tool Installations"
 
# Function to print status
check_cmd() {
  CMD=$1
  DESC=$2
  echo -n "🔹 $DESC: "
  if command -v $CMD >/dev/null 2>&1; then
    echo "✅ Installed"
    $CMD --version 2>/dev/null | head -n 1
  else
    echo "❌ NOT Installed"
  fi
}
 
echo "==============================="
 
check_cmd hadoop "Hadoop"
check_cmd yarn "YARN"
check_cmd spark-shell "Spark Shell"
check_cmd hive "Hive"
check_cmd airflow "Airflow"
check_cmd hue "Hue (Check by web UI)"
check_cmd oozie "Oozie"
check_cmd sqoop "Sqoop"
check_cmd kafka-topics.sh "Kafka"
 
echo "==============================="
echo "🌐 Reminder: UI services (Hue, Airflow, Spark UI, Hadoop UI, etc.) must be started and tested via port forwarding after verification."
