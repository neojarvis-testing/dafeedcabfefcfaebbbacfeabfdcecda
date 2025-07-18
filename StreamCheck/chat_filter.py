from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType, BooleanType

# Load bad words
with open("profanity_words.txt", "r") as f:
    BAD_WORDS = set(word.strip().lower() for word in f.readlines())

# UDFs
def contains_profanity(message):
    words = message.lower().split()
    return any(word in BAD_WORDS for word in words)

def format_alert(message):
    username = message.split(":")[0] if ":" in message else "Unknown"
    return f"[ALERT] Profanity from {username}: \"{message}\""

profanity_udf = udf(contains_profanity, BooleanType())   # ✅ MUST return BooleanType
alert_udf = udf(format_alert, StringType())

# Spark setup
spark = SparkSession.builder.appName("StructuredChatProfanityFilter").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

# Read socket stream
lines = spark.readStream.format("socket").option("host", "localhost").option("port", 9999).load()

# Filter + alert formatting
alerts = lines.filter(profanity_udf(col("value"))).withColumn("alert", alert_udf(col("value"))).select("alert")

# Print only alerts
def show_alerts(df, _):
    for row in df.collect():
        print(row.alert)

# Stream
query = alerts.writeStream.foreachBatch(show_alerts).outputMode("append").start()
query.awaitTermination()
