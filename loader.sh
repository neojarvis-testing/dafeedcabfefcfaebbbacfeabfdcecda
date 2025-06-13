#!/bin/bash

# Define the URL (update if hosted remotely)
AIRFLOW_URL="http://localhost:8080/health"

# Send a GET request and check for HTTP 200
response=$(curl -s -o /dev/null -w "%{http_code}" "$AIRFLOW_URL")

if [ "$response" -eq 200 ]; then
  echo "✅ Airflow UI is up and reachable at $AIRFLOW_URL"
else
  echo "❌ Airflow UI is not reachable. HTTP Status: $response"
fi
