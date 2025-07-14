import findspark
findspark.init()
from pyspark import SparkContext
from pyspark.streaming import StreamingContext

sc = SparkContext("local[2]", "SocketWordCount")
ssc = StreamingContext(sc, 5)  # 5-second batches

lines = ssc.socketTextStream("localhost", 9999)
words = lines.flatMap(lambda line: line.split(" "))
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a, b: a + b)

word_counts.pprint()

ssc.start()
ssc.awaitTermination()
