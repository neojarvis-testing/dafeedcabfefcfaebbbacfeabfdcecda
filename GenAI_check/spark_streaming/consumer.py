from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType

# 1. Define schema
schema = StructType() \
    .add("txn_id", StringType()) \
    .add("timestamp", StringType()) \
    .add("txn_type", StringType()) \
    .add("amount", DoubleType()) \
    .add("source_account", StringType()) \
    .add("dest_account", StringType()) \
    .add("status", StringType()) \
    .add("ip_address", StringType()) \
    .add("device_id", StringType())

# 2. Create Spark session
spark = SparkSession.builder \
    .appName("TransactionStreamConsumer") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 3. Read from Kafka topic
df_kafka_raw = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .option("startingOffsets", "latest") \
    .load()

# 4. Parse value column as JSON
df_parsed = df_kafka_raw.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# 5. Output to console for now
query = df_parsed.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
