# Importing/Adding New Data to an Existing Table

## Importing new data using a Pandas script

Lake Formation tables are registered to a particular S3 directory, not a file. So, for example, if a table is registered to the `s3://lake-formation/data/` and set to the parquet format, all `.parquet` files in that directory will part of table's data.

In summary, to add new data to an existing table, upload the dataframe file(s) (such as `.parquet` format) to a table's S3 data location. Use the program described [here](../transformations_with_pandas) to upload a parquet file to S3.

<br>

## Inserting New Data Using Amazon Athena

You can insert new data using the SQL query `INSERT INTO`

Example query:

```sql
INSERT INTO "database_name"."table_name" VALUES(value1, value2, value3, ...)
```

This can be done manually in the [**Athena query editor**](https://console.aws.amazon.com/athena/home#query) or with a script such as:

### [**`app.py`**](./app.py)
```python
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
```

To run the above script:

* Make sure you're logged into AWS: `aws-azure-login`
* Create a python virtual environment: `python3.8 -m venv venv`
* Activate the virtual environment: `. venv/bin/activate`
* Install the dependencies: `python3.8 -m pip install -r requirements.txt`
* Run the app: `python3.8 app.py`
