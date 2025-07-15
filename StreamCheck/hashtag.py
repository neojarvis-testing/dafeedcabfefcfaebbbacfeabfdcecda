# spark_hashtag_counter.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col
import pandas as pd

# Set up Spark session
spark = SparkSession.builder \
    .appName("HashtagTrendAnalyzer") \
    .getOrCreate()

# Optional: suppress Spark internal logs to reduce clutter
spark.sparkContext.setLogLevel("ERROR")

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "tweets") \
    .load()

lines = df.selectExpr("CAST(value AS STRING)")

hashtags = lines.select(
    explode(split(col("value"), " ")).alias("word")
).filter(col("word").startswith("#"))

# Track batch number
batch_id = {"count": 0}

def show_batch(batch_df, epoch_id):
    batch_id["count"] += 1
    print(f"\n--- Batch: {batch_id['count']} ---")
    result_df = batch_df.groupBy("word").count().orderBy("count", ascending=False)
    result_df.show(truncate=False)

# Attach foreachBatch logic
query = hashtags.writeStream \
    .foreachBatch(show_batch) \
    .outputMode("append") \
    .start()

# Let it run for 60 seconds
query.awaitTermination(60)
