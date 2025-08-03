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

# Script generated for node accelerometer_landing
accelerometer_landing_node1754210991535 = glueContext.create_dynamic_frame.from_catalog(database="singarq_stedi_db", table_name="accelerometer_landing", transformation_ctx="accelerometer_landing_node1754210991535")

# Script generated for node customer_trusted
customer_trusted_node1754211019303 = glueContext.create_dynamic_frame.from_catalog(database="singarq_stedi_db", table_name="customer_trusted", transformation_ctx="customer_trusted_node1754211019303")

# Script generated for node Join
Join_node1754211036335 = Join.apply(frame1=accelerometer_landing_node1754210991535, frame2=customer_trusted_node1754211019303, keys1=["user"], keys2=["email"], transformation_ctx="Join_node1754211036335")

# Script generated for node drop_fields_and_duplicated
SqlQuery0 = '''
select 
    DISTINCT user,
    timeStamp,
    x,
    y,
    z
from myDataSource;
'''
drop_fields_and_duplicated_node1754211321415 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":Join_node1754211036335}, transformation_ctx = "drop_fields_and_duplicated_node1754211321415")

# Script generated for node customer_curated
EvaluateDataQuality().process_rows(frame=drop_fields_and_duplicated_node1754211321415, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1754210979688", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
customer_curated_node1754211064303 = glueContext.getSink(path="s3://singarq-lake-house/customer/curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="customer_curated_node1754211064303")
customer_curated_node1754211064303.setCatalogInfo(catalogDatabase="singarq_stedi_db",catalogTableName="customer_curated")
customer_curated_node1754211064303.setFormat("json")
customer_curated_node1754211064303.writeFrame(drop_fields_and_duplicated_node1754211321415)
job.commit()
