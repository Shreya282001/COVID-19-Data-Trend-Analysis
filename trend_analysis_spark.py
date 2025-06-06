from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date, sum, lag, avg, count
from pyspark.sql.window import Window

# Initializing Spark Session
spark = SparkSession.builder \
    .appName("COVID-19 Trend Analysis") \
    .getOrCreate()

# Loading Data
data_path = "C:\Users\91814\Desktop\Cloud Computing\CC\covid19_dataset.csv"  # Use wildcard for daily files
df = spark.read.csv(data_path, header=True, inferSchema=True)

# Data Preprocessing
df = df.withColumnRenamed("Country/Region", "Country_Region") \
       .withColumnRenamed("Last Update", "Last_Update") \
       .withColumn("Date", to_date(col("Last_Update")))

# Aggregating Data
agg_df = df.groupBy("Date", "Country_Region") \
    .agg(
        sum("Confirmed").alias("Total_Confirmed"),
        sum("Deaths").alias("Total_Deaths"),
        sum("Recovered").alias("Total_Recovered")
    )

# Calculating Daily Changes
window_spec = Window.partitionBy("Country_Region").orderBy("Date")
daily_trends_df = agg_df.withColumn("Daily_Confirmed", col("Total_Confirmed") - lag("Total_Confirmed", 1).over(window_spec)) \
    .withColumn("Daily_Deaths", col("Total_Deaths") - lag("Total_Deaths", 1).over(window_spec)) \
    .withColumn("Daily_Recovered", col("Total_Recovered") - lag("Total_Recovered", 1).over(window_spec))

# Calculating 7-day Moving Average
ma_df = daily_trends_df.withColumn("7_Day_Avg_Confirmed", avg("Daily_Confirmed").over(window_spec.rowsBetween(-6, 0))) \
    .withColumn("7_Day_Avg_Deaths", avg("Daily_Deaths").over(window_spec.rowsBetween(-6, 0))) \
    .withColumn("7_Day_Avg_Recovered", avg("Daily_Recovered").over(window_spec.rowsBetween(-6, 0)))

# Saving Data
output_path = "output/trend_data"
ma_df.write.csv(output_path, header=True, mode="overwrite")

# Stop Spark Session
spark.stop()