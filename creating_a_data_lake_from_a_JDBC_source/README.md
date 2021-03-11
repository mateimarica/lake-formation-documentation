# Creating a data lake from a JDBC source

1. [Create a connection in AWS Glue](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-connection.html). For reference, the JDBC URL format depends on the DBMS. Example: [formatting for a PostgreSQL JDBC URL.](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING)

2. [Create an Amazon S3 Bucket for the Data Lake](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-create-bucket.html). Note that S3 Bucket names have to be *globally* unique.

3. [Register an Amazon S3 Path in Lake Formation](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-register.html)

4. [Grant Data Location Permissions](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-data-location.html)

5. [Create a Database in the Data Catalog](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-create-db.html)

6. [Grant Data Permissions](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-grant-data-permissions.html)

7. [Use a Blueprint to Create a Workflow](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-create-workflow.html)

8. [Run the Workflow](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-run-workflow.html)

9. [Grant SELECT on the Tables](https://docs.aws.amazon.com/lake-formation/latest/dg/tut-grant-select.html)

<br>

## Querying the table in Amazon Athena

Sample query:

1. Go to the [Amazon Athena querying page](https://console.aws.amazon.com/athena/home#query).

2. Select the following:

   * For **Data source**, select `AwsDataCatalog`
   * For **Database**, select your Lake Formation database

3. Under **Tables**, find the table that you just created and click on the three dots **⋮** to the right of the name, and click on **Preview table**. 

    This will generate and execute a query that returns the first 10 rows of in the table.

<br>

---

<br>

Note: This guide is a summarized version of [this tutorial](https://docs.aws.amazon.com/lake-formation/latest/dg/getting-started-tutorial.html)