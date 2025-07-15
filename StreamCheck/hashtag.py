# hashtag.py
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col
import pandas as pd

# Set up Spark session
spark = SparkSession.builder \
    .appName("HashtagTrendAnalyzer") \
    .getOrCreate()

# Optional: suppress Spark internal logs
spark.sparkContext.setLogLevel("ERROR")

# Read stream from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "tweets") \
    .load()

# Extract tweet text
lines = df.selectExpr("CAST(value AS STRING)")

# Extract hashtags
hashtags = lines.select(
    explode(split(col("value"), " ")).alias("word")
).filter(col("word").startswith("#"))

# Track cumulative counts across batches
global_counts = {}

def show_batch(batch_df, epoch_id):
    global global_counts
    print(f"\n--- Batch: {epoch_id + 1} ---")

    # Count hashtags in current batch
    batch_counts = batch_df.groupBy("word").count().toPandas()

    for _, row in batch_counts.iterrows():
        word = row["word"]
        count = row["count"]
        if word in global_counts:
            global_counts[word] += count
        else:
            global_counts[word] = count

    # Print cumulative hashtag counts
    for word, count in sorted(global_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"| {word:<14} | {count:<6} |")

# Write output using foreachBatch
query = hashtags.writeStream \
    .foreachBatch(show_batch) \
    .outputMode("update") \
    .start()

# Run for 60 seconds
query.awaitTermination(60)


