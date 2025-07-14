import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

# Define schema of the incoming JSON messages
schema = StructType() \
    .add("user_id", StringType()) \
    .add("event_type", StringType()) \
    .add("value", StringType()) \
    .add("timestamp", StringType())

# Create SparkSession
spark = SparkSession.builder \
    .appName("KafkaSparkStream") \
    .master("local[*]") \
    .getOrCreate()

# Read stream from Kafka
kafka_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "noisy-topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Convert 'value' column from binary to string, then parse JSON
parsed_df = kafka_df.selectExpr("CAST(value AS STRING) as json_str") \
    .select(from_json(col("json_str"), schema).alias("data")) \
    .select("data.*")

# Output to console
query = parsed_df.writeStream \
    .outputMode("append") \
    .format("console") \
    .trigger(processingTime="10 seconds") \
    .start()

query.awaitTermination()
