import os
# import boto3
# from botocore.exceptions import ClientError
import logging

import gzip
import base64
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# sns = boto3.client('sns')

TOPIC_ARN = os.environ['ALERTS_TOPIC_ARN']

def lambda_handler(event, context):
    print(json.dumps(event))

    # sns.publish(
    #     TopicArn=TOPIC_ARN,
    #     Message=message,
    #     Subject='⚠️ Scheduled Database Update Failed',
    # )

    return {
        'statusCode': 200,
        'body': 'Success'
    }