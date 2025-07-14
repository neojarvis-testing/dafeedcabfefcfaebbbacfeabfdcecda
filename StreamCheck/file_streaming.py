from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
import os

# Configure paths
INPUT_PATH = "file://" + os.path.abspath("logs")

# Initialize Spark Session and StreamingContext
spark = SparkSession.builder.appName("FileDropMonitor").getOrCreate()
sc = spark.sparkContext
ssc = StreamingContext(sc, batchDuration=5)  # 5-second micro-batch

# Stream from the input directory
lines = ssc.textFileStream(INPUT_PATH)

# Filter for log levels
log_levels = lines.filter(lambda line: any(level in line for level in ["INFO", "ERROR", "WARN"]))

# Count log levels
level_counts = log_levels.map(lambda line: (line.split(" ")[0], 1)) \
                         .reduceByKey(lambda a, b: a + b)

# Display in real-time
level_counts.pprint()

# Start the stream
ssc.start()
ssc.awaitTermination()
