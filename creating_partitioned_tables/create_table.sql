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