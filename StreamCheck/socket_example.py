import findspark
findspark.init()
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[2]", "SquareNumbers")
ssc = StreamingContext(sc, 2)  # 2-second batch interval

# Receive numbers as space-separated string
lines = ssc.socketTextStream("localhost", 9999)

# Convert strings to integers, then square them
numbers = lines.flatMap(lambda line: line.split(" ")) \
               .map(lambda num: int(num)) \
               .map(lambda x: (x, x**2))

# Print original and squared numbers
numbers.pprint()

ssc.start()
ssc.awaitTermination()

