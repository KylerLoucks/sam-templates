import json
import boto3
import logging
import os
import requests
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(event)
    
    request_params = event['detail']['requestParameters']
    bucket_name = request_params['bucketName']
    key = request_params['key']