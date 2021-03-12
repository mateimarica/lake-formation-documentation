## Sample app to apply transformations to a parquet using Pandas

The following code downloads a parquet file from a given S3 bucket, performs several transformations on it, and uploads it into a given S3 bucket.

```python
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
```

The easiest way to use this program is to use a input file containing three input values in the following format:

```
<name of the s3 bucket where the input parquet file is stored>
<path to the parquet file (not including root bucket name)>
<complete path of output s3 bucket, with s3:// in front>
```

Example `input.txt` :
```
spectrum_data_s3
channel_analysis/year=2021/month=2/day=17/sensor_host_id=ABCD_EFGH_002/part-637547345-754724624.snappy.parquet
s3://lakeformation-test/transformed_table/
```

Using the example `input.txt` as input will download the parquet file from `s3://spectrum_data_s3/channel_analysis/year=2021/month=2/day=17/sensor_host_id=ABCD_EFGH_002/part-637547345-754724624.snappy.parquet`, perform several transformations on it, and upload it to the `s3://lakeformation-test/transformed_table/` directory, with an auto-generated name.

<br>

## Running the app

* Make sure you're logged into AWS: `aws-azure-login`
* Create a python virtual environment: `python3.8 -m venv venv`
* Activate the virtual environment: `. venv/bin/activate`
* Install the dependencies: `python3.8 -m pip install -r requirements.txt`
* Run the app: `python3.8 app.py < input.txt`

<br>

## Importing as a table into a Lake Formation database

1. Go to the [**Tables** page](https://console.aws.amazon.com/lakeformation/home#tables) in the Lake Formation console and click [**Create Table**](https://console.aws.amazon.com/lakeformation/home#create-table) in the top-right corner.

2. Under **Table details**:

   * Enter a name for the table.
   * Select the database that you want the table to be associated with.

3. Under **Data store**:

   * For the data location, select **Specified path in my account**
   * For the bucket path, enter the S3 directory that the parquet file is in, not including the file itself. For example: `s3://lakeformation-test/transformed_table/`

4. Under **Data format**:

   * Select **PARQUET**

5. Under **Schema**:
   
   * You have to manually define the schema to be able to query the table.

   * Example: Say you have three columns:

        | Column | Data type |
        | ----------- | ----------- |
        | sensor_host_id | string |
        | analysis_start_time | timestamp |
        | hist_count | int |

        <br>

        To define the above schema, do the following:

        * Click **Add column** > Enter `sensor_host_id` under **Column Name** > Select `string` under **Data type** > Click **Add**
        * Click **Add column** > Enter `analysis_start_time` under **Column Name** > Select `string` under **Data type** > Click **Add**
        * Click **Add column** > Enter `hist_count` under **Column Name** > Select `int` under **Data type** > Click **Add**

        <br>

        ---
        **Note:**
        
        Selecting the `timestamp` data type for a column that was originally a `timestamp` will not work when querying with Amazon Athena. Athena cannot recognize the `timestamp` format from parquet (assumably). The following error appears when querying the table in Athena: 

        `HIVE_BAD_DATA: Field analysis_start_time's type BINARY in parquet is incompatible with type timestamp defined in table schema`

        For reference, `BINARY` is the data type used in Parquet, as noted [here](https://docs.aws.amazon.com/athena/latest/ug/data-types.html).

        However, importing a Parquet into a PostgreSQL table then pulling the table into a Lake Formation table using a workflow correctly displays the `timestamp` data types.

        ---

<br>

6. Click **Submit**. Your new table should be visible on the [Lake Formation tables page](https://console.aws.amazon.com/lakeformation/home#tables).

<br>

## Querying the table in Amazon Athena

Sample query:

1. Go to the [Amazon Athena querying page](https://console.aws.amazon.com/athena/home#query).

2. Select the following:

   * For **Data source**, select `AwsDataCatalog`
   * For **Database**, select your Lake Formation database

3. Under **Tables**, find the table that you just created and click on the three dots **⋮** to the right of the name, and click on **Preview table**. 

    This will generate and execute a query that returns the first 10 rows of in the table.