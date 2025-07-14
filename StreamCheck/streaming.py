import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType

# 1. Create Spark session with Kafka support
spark = SparkSession.builder \
    .appName("FraudTransactionMonitor") \
    .master("local[*]") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# 2. Define schema for incoming JSON data
schema = StructType() \
    .add("branch", StringType()) \
    .add("amount", IntegerType()) \
    .add("type", StringType())

# 3. Read from Kafka topic "transactions"
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "transactions") \
    .load()

# 4. Convert binary value to string and parse JSON
parsed = df.selectExpr("CAST(value AS STRING) as json") \
    .select(from_json(col("json"), schema).alias("data")) \
    .select("data.*")

# 5. Filter suspicious transactions
suspicious = parsed.filter(col("amount") > 50000)

# 6. Output to console
query = suspicious.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

query.awaitTermination()
