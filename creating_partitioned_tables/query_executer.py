import boto3

client = boto3.client('athena')

# Change these values to reflect your database & table
database_name = 'lakeformation_test'
table_name = 'partitioned_table'

# Get query from file, using redirection operator
query = input("")

# Execute the query
response = client.start_query_execution(
	QueryString=query,
	QueryExecutionContext={
		'Database': database_name,
		'Catalog': 'AwsDataCatalog'
	},
	ResultConfiguration={
		# This is the S3 location where you want to save the query results. 
		# Can be anywhere in S3.
		'OutputLocation': 's3://lakeformation_test_s3/query_results'
	}
)

print(response)