from aws_lambda_powertools import Tracer, Logger
tracer = Tracer()
logger = Logger()

from s3_service import S3Service

s3 = S3Service()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    logger.info("hello world!")