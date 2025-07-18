from pyspark import SparkContext
from pyspark.streaming import StreamingContext

# Load bad words
with open("profanity_words.txt", "r") as f:
    bad_words = set(word.strip().lower() for word in f.readlines())

def filter_profanity(line):
    words = line.strip().lower().split()
    return any(word in bad_words for word in words)

def extract_username(line):
    if ":" in line:
        return line.split(":")[0]
    return "Unknown"

if __name__ == "__main__":
    sc = SparkContext(appName="ChatProfanityFilter")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 2)
    
    # Listen on all interfaces (important!)
    lines = ssc.socketTextStream("0.0.0.0", 9999)

    def alert_only(rdd):
        for line in rdd.collect():
            if filter_profanity(line):
                username = extract_username(line)
                print(f"[ALERT] Profanity detected from {username}: \"{line}\"")

    lines.foreachRDD(alert_only)

    ssc.start()
    ssc.awaitTermination()
