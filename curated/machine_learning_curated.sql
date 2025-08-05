CREATE EXTERNAL TABLE `machine_learning_curated`(
  `serialnumber` string COMMENT 'from deserializer', 
  `sensorreadingtime` bigint COMMENT 'from deserializer', 
  `distancefromobject` int COMMENT 'from deserializer', 
  `user` string COMMENT 'from deserializer', 
  `timestamp` bigint COMMENT 'from deserializer', 
  `x` double COMMENT 'from deserializer', 
  `y` double COMMENT 'from deserializer', 
  `z` double COMMENT 'from deserializer')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://singarq-lake-house/machine_learning/curated/'
TBLPROPERTIES (
  'CreatedByJob'='machine_learning_curated', 
  'CreatedByJobRun'='jr_cc50ed53b3685a7c953d9ca671588fffe61b7a8a4b6536063b7f3f0d43c995f1', 
  'classification'='json')
