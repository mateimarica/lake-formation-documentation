# Desc: General script for querying on Amazon Athena
# Usage:
# python3.8 query_executor
#
# Output: Query results saved in query_results.json in current directory

import boto3
import time
import sys
import json

client = boto3.client('athena')

# Get input from user
if (len(sys.argv) > 1):
	input_file = open(sys.argv[1], "r")
	query = input_file.read()
	input_file.close()

	print(f"> SQL query read from {sys.argv[1]}")

else:
	query = input("Enter the SQL query: ")

database_name = input("Enter the name of the database: ")
output_location = input("Enter the S3 URI of where to store the query results: ")

# Begin the execution of the query
response = client.start_query_execution(
	QueryString=query,
	QueryExecutionContext={
		'Database': database_name,
		'Catalog': 'AwsDataCatalog'
	},
	ResultConfiguration={
		'OutputLocation': output_location
	}
)

# Loop on query status until it's done, because getting the query results before it's done will cause an exception
while(True):

	# 2-4 seconds is usually long enough for the average query, tweak as needed
	time.sleep(2)

	status = client.get_query_execution(
		QueryExecutionId=response['QueryExecutionId']
	)

	state = status['QueryExecution']['Status']['State']

	if (state == 'SUCCEEDED'):
		break

	if (state == 'FAILED'):
		raise client.exceptions.InvalidRequestException(status['QueryExecution']['Status']['StateChangeReason'])

	print("Waiting for query to finish...")

# Returns the results of the query
results = client.get_query_results(
	QueryExecutionId=response['QueryExecutionId'],
	MaxResults=100
)

OUTPUT_FILE_NAME = 'query_results.json'

# Write results to file
f = open(OUTPUT_FILE_NAME, "w")
f.write(json.dumps(results))
f.close()

print("Output written to " + OUTPUT_FILE_NAME)