from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F

def get_spark() -> SparkSession:
  spark_builder = SparkSession.builder
  return spark_builder.appName('dab_test_clean').getOrCreate()


def clean_and_write_carrier(spark: SparkSession) -> DataFrame:
  df = spark.read.table("datalake_silver.carrier")
  cleaned_df = df.select("*").withColumn("__id", F.monotonically_increasing_id())
  cleaned_df.write.format("parquet").mode("overwrite") \
    .save("s3://bucket_example/databricks_dab_test/data/outputs/clean/carrier")


def clean_and_write_category(spark: SparkSession) -> DataFrame:
  df = spark.read.table("datalake_silver.category")
  #df = spark.read.format("parquet").load("./data/inputs/category")
  cleaned_df = df.select("*").withColumn("__id", F.monotonically_increasing_id())
  cleaned_df.write.format("parquet").mode("overwrite") \
    .save("s3://bucket_example/databricks_dab_test/data/outputs/clean/carrier")


def clean():
  spark = get_spark()
  clean_and_write_carrier(spark)
  clean_and_write_category(spark)


if __name__ == '__main__':
  clean()