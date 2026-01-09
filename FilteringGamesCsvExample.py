import sys
assert sys.version_info >= (3, 8)

from pyspark.sql import SparkSession, types

# Use spark to filter the simulated games for model 4

Data_Schema = types.StructType([
    types.StructField('Result', types.StringType()),
    types.StructField('Moves', types.StringType()),
])

# Use spark to filter the simulated games for model 4
def main(games_directory, output_directory):
    df = spark.read.csv(games_directory, header=True, schema=Data_Schema)
    wins = df.filter(df["Result"] == "1-0")

    wins.write.csv(output_directory, header=True, mode="overwrite")

if __name__ == '__main__':
    games_directory = sys.argv[1]
    output_directory = sys.argv[2]
    spark = SparkSession.builder.appName('simulated filtering').getOrCreate()
    assert spark.version >= '3.2'
    spark.sparkContext.setLogLevel('WARN')
    main(games_directory, output_directory)
