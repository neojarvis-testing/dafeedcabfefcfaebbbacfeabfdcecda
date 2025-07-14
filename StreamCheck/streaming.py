import findspark
findspark.init()
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext

spark = SparkSession.builder.appName("ClickstreamAnalytics").getOrCreate()
sc = spark.sparkContext
ssc = StreamingContext(sc, 5)

# Create DStream from socket
lines = ssc.socketTextStream("localhost", 9999)

# DEBUG: Show raw input
lines.pprint()

# Parse path and count
paths = lines.map(lambda line: line.strip().split()[-1] if len(line.strip().split()) > 1 else "/unknown")
path_counts = paths.map(lambda path: (path, 1)).reduceByKey(lambda a, b: a + b)

# Show output
path_counts.pprint()

ssc.start()
ssc.awaitTermination()
