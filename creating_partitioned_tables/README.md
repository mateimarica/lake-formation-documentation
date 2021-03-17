# Partitioning Data

Data partitioning in Athena is purely based on the S3 directory structure.

Partitions are defined by an S3 directory's name, a key-value pair. For example, a database table partitioned by **year** could have a directories named `year=2019`, `year=2020`, and `year=2021`.

<br>

## Creating a partitioned table in AWS Lake Formation

1. Have a Lake Formation database that uses proper naming conventions: **the only special characters that a database name should have are underscores** (_). It will let you create a database with a name with other special characters, but doing so [will cause problems when querying with Amazon Athena](https://aws.amazon.com/premiumsupport/knowledge-center/parse-exception-missing-eof-athena/).

	If you don't already have a database in Lake Formation, head over [here](https://console.aws.amazon.com/lakeformation/home#create-database) and create one. Give it a name according to the guidelines above and leave everything else alone.

	Example of a valid database name: `lakeformation_test_db`

<br>

2. Add parquet files to an S3 bucket with a partitioned directory structure.
	
	For this example, we will use a bucket named `lakeformation_test_s3`. For our partitioned table, we will use the directory `s3://lakeformation_test_s3/partitioned_table/`, which will be partitioned by year, month, day.

	<br>

	How the directory directory structure could look: (parquet file names are randomly generated)

	```
	lakeformation_test_s3
	|
	└───partitioned_table
		|
		├───year=2020
		|	|
		|	└───month=12
		|		|
		|		├───day=5
		|		|	|
		|		|	├───54833483.parquet
		|		|	|
		|		|	└───15983948.parquet
		|		|
		|		└───day=7
		|			|
		|			└───72324212.parquet
		|
		├───year=2021
		|
		|
		...
	```

	Luckily, you don't have to manually define such a directory structure. If you have a script that uploads parquet files to a particular directory based on a date, it will create any directories that don't already exist.

	See [this script](../transformations_with_pandas/README.md#sample-app-to-apply-transformations-to-a-parquet-using-pandas). See how the parquet files are uploaded to S3, using the `awswrangler.s3.to_parquet` function. For example, if you wanted convert and upload your dataframe as a parquet file on December 15, 2020, you would set the `path` argument to `'s3://lakeformation_test_s3/partitioned_table/year=2020/month=12/day=15/'`

	<br>

3. Create the partitioned table.

	We already have the directory structure set up for our `partitioned_table` table. Now we have to actually create it, using an SQL query:

	### [`create_table.sql`](./create_table.sql)
	```sql
	CREATE EXTERNAL TABLE `partitioned_table` (
		`column1` string, 
		`column2` int,
		`column3` string
	)
	PARTITIONED BY ( 
		`year` int, 
		`month` int, 
		`day` int
	)
	ROW FORMAT SERDE 
		'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
	STORED AS INPUTFORMAT 
		'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
	OUTPUTFORMAT 
		'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
	LOCATION
		's3://lakeformation_test/partitioned_table/'
	TBLPROPERTIES (
		'CrawlerSchemaDeserializerVersion'='1.0', 
		'CrawlerSchemaSerializerVersion'='1.0', 
		'classification'='parquet', 
		'compressionType'='none', 
		'typeOfData'='file'
	);
	```

	Change the columns and S3 location in the above SQL query to fit your situation.

	<br>

	This query can be entered manually in the [**Athena query editor**](https://console.aws.amazon.com/athena/home#query) or executed with a script such as:

	### [`query_executer.py`](./query_executer.py)
	```python
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
	```

	### Running `query_executer.py`
	*Assuming you have the table creation SQL query in a file named `create_table.sql`*:

	* Make sure you're logged into AWS: `aws-azure-login`
	* Create a python virtual environment: `python3.8 -m venv venv`
	* Activate the virtual environment: `. venv/bin/activate`
	* Install the dependencies: `python3.8 -m pip install -r requirements.txt`
	* Run the app: `python3.8 query_executer.py < create_table.sql`

<br>

4. Before we query the table, we must load the partitions. The following SQL query will do so:

	### [`load_partitions.sql`](./load_partitions.sql)
	```sql
	MSCK REPAIR TABLE partitioned_table;
	```

	This query can be entered manually in the [**Athena query editor**](https://console.aws.amazon.com/athena/home#query) or executed with a script:

	### Running `query_executer.py`

	*Assuming you already activated and set up the virtual environment, as per the previous step:*

	* Run the app: `python3.8 query_executer.py < load_partitions.sql`

<br>

## Querying the Partitioned Table

When you query a table using boto3, it saves the output in a CSV file in the S3 directory we supply in the `OutputLocation` argument when executing a query. The CSV file is named `x.csv`, where `x` is the `QueryExecutionId` value in the dictionary returned by the Athena `client.start_query_execution` function.

For now, it's easier to use the [**Athena query editor**](https://console.aws.amazon.com/athena/home#query) for testing. Enter and execute the following sample SQL query:

### [`select.sql`](./select.sql)
```sql
SELECT column1, year FROM "lakeformation_test"."partitioned_table" 
WHERE month = 3 AND year = 2021
LIMIT 10;
```

Tweak the above query where needed.

Notice how the `year`, `month`, and `day` partitions are treated as columns when querying.