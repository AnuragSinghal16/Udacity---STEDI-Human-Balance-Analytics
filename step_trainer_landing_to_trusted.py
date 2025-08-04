import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node customer_curated
customer_curated_node1754314718072 = glueContext.create_dynamic_frame.from_catalog(database="singarq_stedi_db", table_name="customer_curated", transformation_ctx="customer_curated_node1754314718072")

# Script generated for node step_trainer_landing
step_trainer_landing_node1754314749079 = glueContext.create_dynamic_frame.from_catalog(database="singarq_stedi_db", table_name="step_trainer_landing", transformation_ctx="step_trainer_landing_node1754314749079")

# Script generated for node join_and_step_trainer_fields
SqlQuery0 = '''
select a.* from step_trainer a
inner join customer_curated b 
on a.serialNumber = b.serialnumber;
'''
join_and_step_trainer_fields_node1754314968565 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"customer_curated":customer_curated_node1754314718072, "step_trainer":step_trainer_landing_node1754314749079}, transformation_ctx = "join_and_step_trainer_fields_node1754314968565")

# Script generated for node step_trainer_trusted
EvaluateDataQuality().process_rows(frame=join_and_step_trainer_fields_node1754314968565, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1754312959016", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
step_trainer_trusted_node1754315269551 = glueContext.getSink(path="s3://singarq-lake-house/step_trainer/trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="step_trainer_trusted_node1754315269551")
step_trainer_trusted_node1754315269551.setCatalogInfo(catalogDatabase="singarq_stedi_db",catalogTableName="step_trainer_trusted")
step_trainer_trusted_node1754315269551.setFormat("json")
step_trainer_trusted_node1754315269551.writeFrame(join_and_step_trainer_fields_node1754314968565)
job.commit()
