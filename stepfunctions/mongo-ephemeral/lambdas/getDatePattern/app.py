
import json
from datetime import datetime
from datetime import timezone


def lambda_handler(event, context):
    date_pattern = datetime.now(tz=timezone.utc).strftime('%Y%m%d')

    return {
        'statusCode': 200,
        'datePattern': date_pattern
    }