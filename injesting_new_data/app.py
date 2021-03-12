import boto3

client = boto3.client('athena')

# Change these values to reflect your database & table
database_name = 'database_name'
table_name = 'table_name'

# Put together the query
query = f"""INSERT INTO "{database_name}"."{table_name}" VALUES('hello', 123, 'foo')"""

# Execute the query
response = client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
                'Database': database_name,
                'Catalog': 'AwsDataCatalog'
        },
        ResultConfiguration={
                # This is the S3 location where you want to save the query results
                'OutputLocation': 's3://bucket_name/path/to/query/results'
        }
)

print(response)