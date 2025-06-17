#!/bin/bash
echo "🔍 Checking YARN (Hadoop ResourceManager)..."

# CLI Check
echo "[✔] Cluster Nodes:"
yarn node -list || echo "❌ YARN node list failed"

# Web UI
echo "[🌐] ResourceManager UI: http://localhost:8080/proxy/8088/"
echo "[🌐] NodeManager UI: http://localhost:8080/proxy/8042/"
