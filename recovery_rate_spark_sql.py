from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_date

# Initialize Spark session
spark = SparkSession.builder \
    .appName("COVID-19 Recovery Rate Analysis") \
    .getOrCreate()

def load_data(file_path):
    """
    Load the COVID-19 dataset using Spark.
    """
    try:
        df = spark.read.csv(file_path, header=True, inferSchema=True)
        return df
    except Exception as e:
        raise Exception(f"Error loading data: {e}")

def preprocess_data(df):
    """
    Preprocess the data:
    - Convert 'Last_Update' to date format
    - Register the DataFrame as a temporary SQL table
    """
    df = df.withColumn("Last_Update", to_date(col("Last_Update")))  # Convert to date
    df.createOrReplaceTempView("covid_data")  # Register table for SQL queries
    return df

def calculate_global_recovery_rate():
    """
    Calculate global recovery rates using Spark SQL.
    """
    query = """
    SELECT
        Country_Region,
        Last_Update,
        SUM(Recovered) AS total_recovered,
        SUM(Confirmed) AS total_confirmed,
        CASE
            WHEN SUM(Confirmed) > 0 THEN
                LEAST(SUM(Recovered), SUM(Confirmed)) / SUM(Confirmed)
            ELSE 0
        END AS recovery_rate
    FROM
        covid_data
    GROUP BY
        Country_Region, Last_Update
    ORDER BY
        Last_Update
    """
    return spark.sql(query)

def calculate_recovery_rate_by_country(country):
    """
    Calculate recovery rates for a specific country using Spark SQL.
    """
    query = f"""
    SELECT
        Last_Update,
        SUM(Recovered) AS total_recovered,
        SUM(Confirmed) AS total_confirmed,
        CASE
            WHEN SUM(Confirmed) > 0 THEN
                LEAST(SUM(Recovered), SUM(Confirmed)) / SUM(Confirmed)
            ELSE 0
        END AS recovery_rate
    FROM
        covid_data
    WHERE
        Country_Region = '{country}'
    GROUP BY
        Last_Update
    ORDER BY
        Last_Update
    """
    return spark.sql(query)

