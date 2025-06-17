#!/bin/bash
echo "🔍 Checking Spark..."

# CLI Check
echo "[✔] Running Spark Pi job:"
spark-submit --class org.apache.spark.examples.SparkPi \
  $SPARK_HOME/examples/jars/spark-examples*.jar 10 || echo "❌ Spark job failed"

bash /opt/spark/sbin/start-history-server.sh

# Web UI
echo "[🌐] Spark Driver UI: http://localhost:8080/proxy/4040/"
echo "[🌐] Spark History Server UI: http://localhost:8080/proxy/18080/"
