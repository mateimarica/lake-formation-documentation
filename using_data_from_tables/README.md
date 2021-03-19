# Consume/Using Data from Tables

## Using a Python script

When using boto3 to query from Amazon Athena, the query's result set will be returned as a Python dictionary:

```python
{
    'UpdateCount': 123,
    'ResultSet': {
        'Rows': [
            {
                'Data': [
                    {
                        'VarCharValue': 'string'
                    },
                ]
            },
        ],
        'ResultSetMetadata': {
            'ColumnInfo': [
                {
                    'CatalogName': 'string',
                    'SchemaName': 'string',
                    'TableName': 'string',
                    'Name': 'string',
                    'Label': 'string',
                    'Type': 'string',
                    'Precision': 123,
                    'Scale': 123,
                    'Nullable': 'NOT_NULL'|'NULLABLE'|'UNKNOWN',
                    'CaseSensitive': True|False
                },
            ]
        }
    },
    'NextToken': 'string'
}
```
[^ Source](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/athena.html#Athena.Client.get_query_results)

<br>

So we already have a script that returns a Athena query's result-set and saves it as JSON file ([query_executer.py](../query_executer.py)). Now that we see how the result set is formatted, we can write a script to interact with the data.

### [`data_printer.py`](./data_printer.py)

Here's an example script that just prints out the data from the JSON file.

```python
import json

# Convert JSON input to Python dictionary
results = json.loads(input())

for row in results['ResultSet']['Rows']:
	for column in row['Data']:
		print(column['VarCharValue'] + "\t", end="")
	
	# Goes to next line
	print()
```

<br>

## Example Usage

Let's say we have a database table that:
* is named `partitoned` 
* is part of the `lakeformation_test_db` database
* is partitioned by year, month, day
* has several columns, one of which is named `analysis_start_time`


```console
$ python ../query_executer.py
Enter the SQL query: SELECT analysis_start_time, month FROM "partitioned" WHERE month = 3 LIMIT 3;
Enter the name of the database: lakeformation_test_db
Enter the S3 URI of where to store the query results: s3://lakeformation-test-query-results
Waiting for query to finish...
Output written to query_results.json
$ 
```

> **Note:** The reason we do `../query_executer.py` is because we assume that the current directory is the directory of this README file, and query_executer.py is saved in the root directory.

<br>

So, `query_executer.py` has outputted a file named `query_results.json`. Now let's funnel that JSON file into `data_printer.py`:

```console
$ python data_printer.py < query_results.json
analysis_start_time     month
2021-03-11 00:00:00     3
2021-03-11 00:00:00     3
2021-03-11 00:00:00     3
$ 
```

As we can see, the data came out as predicted. We querying only the data when `month = 3`, so that's all we got. 

Just to note, this output would be a lot uglier if the timestamp of `analysis_start_time` wasn't the same length as the column name.