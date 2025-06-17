#!/bin/bash
echo "🔍 Checking Sqoop..."

# Dummy check: test connection to a local MySQL/PostgreSQL DB
sqoop list-databases \
  --connect jdbc:mysql://localhost:3306/ \
  --username root --password examly \
  || echo "❌ Sqoop DB connection failed"

echo "[ℹ️] Sqoop has no Web UI."
