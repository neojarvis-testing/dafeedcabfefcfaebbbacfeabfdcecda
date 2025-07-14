import findspark
findspark.init()
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json

sc = SparkContext("local[2]", "FraudDetector")
ssc = StreamingContext(sc, 5)  # 5-second batch interval

# Kafka stream via Zookeeper
kafka_stream = KafkaUtils.createStream(
    ssc,
    "localhost:2181",          # Zookeeper address
    "transaction-group",       # Consumer group
    {"transactions": 1}        # Topic map
)

# Parse and filter suspicious transactions
transactions = kafka_stream.map(lambda msg: json.loads(msg[1]))
suspicious = transactions.filter(lambda txn: txn["amount"] > 50000)
suspicious.pprint()

ssc.start()
ssc.awaitTermination()
