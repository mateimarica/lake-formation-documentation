## Transformations with Glue jobs

*This is an alternative method to using Pandas to transform datasets, however this method causes error for unknown reasons.*

A Glue job can be used to *extract, transform, and load* (ETL) a dataset. The easiest way to do so appears to be use the visual [Glue Studio](https://console.aws.amazon.com/gluestudio/home#/jobs) editor.

1. Under **Create job**:

    * Select **Source and target added to the graph**
    * For **Source**, select **S3**
    * For **Target**, select **Glue Data Catalog**

2. Select the **Data source** block. 
    * On the **Data source properties - S3** tab:
        * Under **S3 source type**, select **S3 location**
        * Under **S3 URL**, enter the full S3 path of the parquet file.
        * Under **Data format**, select **Parquet**

    * On the **Output schema** tab, click **↻ Infer schema**. The table's schema should appear.

3. Select the **Transform** block.
    * On the **Transform** tab, you can do some simple data transformations, like renaming columns, changing column data types, or dropping columns. After applying the transformations, go to the **Output schema** tab to check what the output will look like.

4. Select the **Data target** block.
    * On the **Data target properties - AWS Glue Catalog** tab:
        * Under **Database**, select your Lake Formation database's name.
        * Under **Table**, select the table that you want the transformed dataset to be put into.
            * If you don't have such a table, head over to the [**Create table**](https://console.aws.amazon.com/lakeformation/home#create-table) page in Lake Formation. Select your database and give the table a name, then click  **Submit** at the bottom of the page. Head back to the visual Glue editor and select your new table, but you may have to refresh the page for it to appear.
        * Under **Data Catalog update options**, select **Update schema and add new partitions**.

5. Click on the **Job details** tab in the top-left corner. Under **IAM Role**, select **LakeFormationWorkflowRole**. 

    *Note: I don't know if this the correct role, since I suspect the eventual errors are caused by permission issues.*

6. Save the Glue job by clicking **Save** in the top-right corner.

7. Click on the **Runs** tab in the top-left corner. This is where all the job runs are shown. Click the **Run** button in the top-right to run the job.

<br>

---

<br>

When running this job, you will likely get the error `An error occurred while calling o95.pyWriteDynamicFrame. Failed to load format with name parquet`. I'm not sure what causes this, but it's likely to do with lack of S3 permissions in the LakeFormationWorkflowRole. 

In the CloudWatch logs, the following exception is visible: 

`Caused by: com.amazon.ws.emr.hadoop.fs.shaded.com.amazonaws.services.s3.model.AmazonS3Exception: Access Denied`

So it's unclear as to which action the IAM role does not have permission for.

<br>

---