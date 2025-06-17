#!/bin/bash
echo "Starting Hadoop daemons..."
hdfs --daemon start namenode
hdfs --daemon start datanode
hdfs --daemon start secondarynamenode
yarn --daemon start resourcemanager
yarn --daemon start nodemanager
echo "Hadoop started!"
 
echo "🔍 Checking Hadoop..."
 
# CLI Check
echo "[✔] Listing HDFS root directory:"
hdfs dfs -ls / || echo "❌ HDFS not responding"