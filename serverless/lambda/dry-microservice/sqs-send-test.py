import boto3
import json
from aws_lambda_powertools import Logger

logger = Logger()

sqs = boto3.client('sqs', region_name="us-east-1")

queue_url = "https://sqs.us-east-1.amazonaws.com/570351108046/lambda-dry-microservice-queue"

request = {
    "testing": "this is a test event"
}

# Send to SQS queue
try: 
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=json.dumps(request)
    )
    logger.info(f"Successfully delivered to SQS! Message ID: {response['MessageId']}")
except Exception as e:
    logger.exception(f"Error sending to SQS queue: {e}")
    raise