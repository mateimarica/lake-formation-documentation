# Importing/Adding New Data to an Existing Table

## Importing new data using a Pandas script

Lake Formation tables are registered to a particular S3 directory, not a file. So, for example, if a table is registered to the `s3://lake-formation/data/` and set to the parquet format, all `.parquet` files in that directory will be a part of the table's data.

In summary, to add new data to an existing table, upload the dataframe file(s) (such as `.parquet` format) to a table's S3 data location. Use the program described [here](../transformations_with_pandas) to upload a parquet file to S3.

<br>

## Inserting New Data Using Amazon Athena

You can insert new data using the SQL query `INSERT INTO`

Example query:

```sql
INSERT INTO "database_name"."table_name" VALUES(value1, value2, value3, ...)
```

This can be done manually in the [**Athena query editor**](https://console.aws.amazon.com/athena/home#query) or with a script such as:

### Running [`query_executer.py`](../query_executer)

* Make sure you're logged into AWS: `aws-azure-login`
* Create a python virtual environment: `python3.8 -m venv venv`
* Activate the virtual environment: `. venv/bin/activate`
* Install the dependencies: `python3.8 -m pip install -r requirements.txt`
* Run the app: `python3.8 ../query_executer.py`
