# clickstream_socket_example.py
import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

# Setup Spark and Streaming
spark = SparkSession.builder.appName("ClickstreamAnalytics").getOrCreate()
sc = spark.sparkContext
ssc = StreamingContext(sc, batchDuration=5)

# Create DStream from socket
lines = ssc.socketTextStream("localhost", 9999)

# Parse page path and count clicks
paths = lines.map(lambda line: line.strip().split()[-1])  # Get last word (URL path)
path_counts = paths.map(lambda path: (path, 1)).reduceByKey(lambda a, b: a + b)

# Display output
path_counts.pprint()

# Start the stream
ssc.start()
ssc.awaitTermination()
