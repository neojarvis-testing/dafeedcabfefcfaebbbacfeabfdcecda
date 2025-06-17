#!/bin/bash

echo "🔍 Verifying Big Data Tools Readiness"
echo "--------------------------------------"

# Hadoop - HDFS root listing
echo "📦 HADOOP"
hdfs dfs -ls / >/dev/null 2>&1 && echo "✔ Hadoop HDFS is responsive" || echo "❌ Hadoop HDFS check failed"

# Spark - version & history directory check
echo -e "\n⚡ SPARK"
spark-submit --version >/dev/null 2>&1 && echo "✔ Spark CLI is accessible" || echo "❌ Spark CLI check failed"
[ -d /tmp/spark-events ] && echo "✔ Spark event log directory exists" || echo "⚠ Missing Spark log dir"

# Hive - basic query
echo -e "\n🐝 HIVE"
echo "SHOW DATABASES;" | hive -S >/dev/null 2>&1 && echo "✔ Hive metastore is working" || echo "❌ Hive shell failed"

# Sqoop - list MySQL DBs
echo -e "\n🔁 SQOOP"
sqoop list-databases --connect jdbc:mysql://localhost:3306/ --username root --password examly >/dev/null 2>&1 && \
echo "✔ Sqoop connected to MySQL" || echo "❌ Sqoop MySQL connection failed"

# Kafka - list topics
echo -e "\n🟠 KAFKA"
kafka-topics.sh --list --bootstrap-server localhost:9092 >/dev/null 2>&1 && echo "✔ Kafka broker responsive" || echo "❌ Kafka broker not reachable"

# Airflow - list DAGs
echo -e "\n🧭 AIRFLOW"
airflow dags list >/dev/null 2>&1 && echo "✔ Airflow CLI is responsive" || echo "❌ Airflow CLI failed"

echo -e "\n✅ Big Data Tools Check Completed."
