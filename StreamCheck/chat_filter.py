from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Load profanity words into a set
with open("profanity_words.txt", "r") as f:
    bad_words = set(word.strip().lower() for word in f.readlines())

def filter_profanity(line):
    words = line.strip().lower().split()
    for word in words:
        if word in bad_words:
            return True
    return False

def extract_username(line):
    if ":" in line:
        return line.split(":")[0]
    return "Unknown"

if __name__ == "__main__":
    sc = SparkContext(appName="ChatProfanityFilter")
    ssc = StreamingContext(sc, 2)  # 2-second batch

    # Connect to Netcat socket
    lines = ssc.socketTextStream("localhost", 9999)

    # Filter for profane messages
    flagged = lines.filter(filter_profanity)

    # Format and print flagged messages
    def alert_format(rdd):
        for line in rdd.collect():
            username = extract_username(line)
            print(f"[ALERT] Profanity detected from {username}: \"{line}\"")

    flagged.foreachRDD(alert_format)

    ssc.start()
    ssc.awaitTermination()
