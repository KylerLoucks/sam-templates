from aws_lambda_powertools import Tracer, Logger
tracer = Tracer()
logger = Logger()

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    logger.info("hello world!")