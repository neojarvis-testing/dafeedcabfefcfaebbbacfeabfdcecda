from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("SalesETL").enableHiveSupport().getOrCreate()

df = spark.read.option("header", "false").csv("hdfs:///user/hueadmin/")
df = df.withColumnRenamed("_c0", "transaction_id") \
       .withColumnRenamed("_c1", "customer_id") \
       .withColumnRenamed("_c2", "amount") \
       .withColumnRenamed("_c3", "sales_date")

# Simple transformation: filter transactions > 1000
df_filtered = df.filter(df.amount > 1000)

# Write to Hive table
df_filtered.write.mode("overwrite").saveAsTable("sales_filtered")