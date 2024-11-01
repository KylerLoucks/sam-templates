import os
import boto3
import logging
from botocore.exceptions import ClientError
import gzip
import base64
import json
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

sns = boto3.client('sns')

TOPIC_ARN = os.environ['ALERTS_TOPIC_ARN']

def lambda_handler(event, context):
    print(json.dumps(event))
    
    # Decode from base64
    compressed_payload = base64.b64decode(event['awslogs']['data'])
    
    # Decompress the payload
    uncompressed_payload = gzip.decompress(compressed_payload)
    
    # Parse the JSON
    log_data = json.loads(uncompressed_payload)
    
    print(json.dumps(log_data))
    
    # Grab the name of the function from the log group name
    log_group = log_data['logGroup']
    match = re.search(r'backend-(.*?)Lambda', log_group.split('/')[-1])
    function_name = match.group(1)

    print(function_name)

    # error_message = log_data['logEvents'][0]['message']
    # msg = { 'message': message }
    
    # print(json.dumps(msg))

    message = f"An error occurred during execution of the '{function_name}' Lambda function!\nThis affects data extraction of the respective exclusion dataset. Please take action accordingly."

    sns.publish(
        TopicArn=TOPIC_ARN,
        Message=message,
        Subject='⚠️ Scheduled Database Update Failed',
    )

    return {
        'statusCode': 200,
        'body': 'Success'
    }