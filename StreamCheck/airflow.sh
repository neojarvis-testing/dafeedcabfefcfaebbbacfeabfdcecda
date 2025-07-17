#!/bin/bash

echo "🔄 Checking & Initializing Airflow..."

# Step 1: Initialize or upgrade the Airflow metadata DB
airflow db migrate

# Step 2: Create default admin user if not already created
echo "👤 Creating default Airflow admin user..."
airflow users create \
  --username airflowadmin \
  --firstname Airflow \
  --lastname Admin \
  --role Admin \
  --email admin@example.com \
  --password airflow123 2>/dev/null || echo "✅ User 'airflowadmin' already exists"

# Step 3: Start the webserver in the background
echo "🚀 Starting Airflow Webserver on port 8080..."
airflow webserver --port 8080 &

# Step 4: Start the scheduler in the background
echo "📅 Starting Airflow Scheduler..."
airflow scheduler &

# Step 5: Optional wait for services to initialize
sleep 10

# Step 6: Run CLI diagnostics
echo "🧪 Validating Airflow Setup..."
airflow db check || echo "❌ Airflow DB not initialized properly"
airflow dags list || echo "❌ Failed to list DAGs"
airflow dags list-import-errors

# Step 7: Final info
echo "🌐 Airflow Web UI should be accessible at: http://localhost:8080/login/"
echo "🔐 Login with → Username: airflowadmin | Password: airflow123"
