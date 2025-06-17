#!/bin/bash
echo "🔍 Checking Hive..."

# CLI Check
echo "[✔] Running Hive shell test:"
echo "SHOW DATABASES;" | hive || echo "❌ Hive shell failed"

# Web UI: Hive does not have a default standalone UI.
echo "[ℹ️] Hive does not provide a standalone Web UI. Use Hue for visual queries."
