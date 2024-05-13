from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F

def get_spark() -> SparkSession:
  try:
    from databricks.connect import DatabricksSession
    spark_builder = DatabricksSession.builder
  
  except ImportError:
    spark_builder = SparkSession.builder

  return spark_builder.appName('dab_test_derived').getOrCreate()


def derived_and_write_carrier(spark: SparkSession) -> DataFrame:
  df = spark.read.format("parquet").load("s3://bucket_example/databricks_dab_test/data/outputs/clean/carrier")
  cleaned_df = df.select("*").withColumn("type", F.lit("derived"))
  cleaned_df.write.format("parquet").mode("overwrite") \
    .save("s3://bucket_example/databricks_dab_test/data/outputs/derived/carrier")


def derived_and_write_category(spark: SparkSession) -> DataFrame:
  df = spark.read.format("parquet").load("s3://bucket_example/databricks_dab_test/data/outputs/clean/category")
  cleaned_df = df.select("*").withColumn("type", F.lit("derived"))
  cleaned_df.write.format("parquet").mode("overwrite") \
    .save("s3://bucket_example/databricks_dab_test/data/outputs/derived/category")


def derived():
  spark = get_spark()
  derived_and_write_carrier(spark)
  derived_and_write_category(spark)


if __name__ == '__main__':
  derived()
