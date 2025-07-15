# spark_hashtag_counter.py
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, col

# Create Spark session
spark = SparkSession.builder \
    .appName("HashtagTrendAnalyzer") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "tweets") \
    .load()

# Extract tweet text
lines = df.selectExpr("CAST(value AS STRING)")

# Extract hashtags
hashtags = lines.select(
    explode(
        split(col("value"), " ")
    ).alias("word")
).filter(col("word").startswith("#"))

# Count hashtags in micro-batches
hashtag_counts = hashtags.groupBy("word").count().orderBy("count", ascending=False)

# Output to console
query = hashtag_counts.writeStream \
    .outputMode("complete") \
    .format("console") \
    .option("truncate", False) \
    .start()

query.awaitTermination()
