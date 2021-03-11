import boto3
import io
import pandas
import re # regex
import awswrangler

input_bucket_name = input("Enter the input bucket name: ")
input_bucket_file_path = input("Enter the path to the parquet file: ")
output_bucket_path = input("Enter the output S3 file path: ")

# Extract sensor_host_id value from the parquet file path
sensor_host_id = re.findall('sensor_host_id=(\w+)\/', bucket_file_path)[0]

# Establish reference to the parquet file in the S3 bucket
s3 = boto3.resource('s3')
data = s3.Object(
        bucket_name=bucket_name,
        key=bucket_file_path
)

# Download the parquet file as an object
buffer = io.BytesIO()
data.download_fileobj(buffer)
dataframe = pandas.read_parquet(buffer)

# Insert a new a column at the front
dataframe.insert(
        loc=0,
        column='sensor_host_id',
        value=sensor_host_id,
        allow_duplicates=False
)

# Drops all columns except the ones listed below
dataframe = dataframe.filter(
        [
                'sensor_host_id',
                'analysis_start_time',
                'hist_count',
        ]
)

# Converts the dataframe to parquet format and saves in a folder in the given S3 Bucket
awswrangler.s3.to_parquet(
        df=dataframe,
        path=output_bucket_path,
        dataset=True
)