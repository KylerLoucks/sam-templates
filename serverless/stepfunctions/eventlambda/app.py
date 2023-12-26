import os
import boto3
from botocore.exceptions import ClientError
import logging

import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)



TOPIC_ARN = os.environ['ALERTS_TOPIC_ARN']
AWS_REGION = os.environ['AWS_REGION']
ACCOUNT_ID = os.environ['AWS_ACCOUNT_ID']
sns = boto3.client('sns')
states = boto3.client("stepfunctions")
def lambda_handler(event, context):
    logger.info(json.dumps(event))

    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/stepfunctions/client/describe_state_machine.html
    response = states.describe_state_machine(
        stateMachineArn=event['detail']['stateMachineArn']
    )

    state_machine_name = response['name']
    state_machine_url = f"https://{AWS_REGION}.console.aws.amazon.com/states/home?region={AWS_REGION}#/statemachines/view/arn%3Aaws%3Astates%3A{AWS_REGION}%3A770085715007%3AstateMachine%3A{state_machine_name}"
    message = f"An error occurred during execution of the '{state_machine_name}' State Machine!\nThis affects data extraction of the respective exclusion dataset. Please take action accordingly.\n\nState Machine URL: {state_machine_url}"

    try:

        sns.publish(
            TopicArn=TOPIC_ARN,
            Message=message,
            Subject='⚠️ Scheduled Database Update Failed',
        )

    except ClientError as e:
        logger.error(f"An error occurred: {e}")
        raise

    return {
        'statusCode': 200,
        'body': "success"
    }