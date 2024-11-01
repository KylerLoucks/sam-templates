import json
import boto3
import os


# sam local invoke dynamoCRUDFunction --event events/CreateCapacityReservation-manualend.json

def lambda_handler(event, context):
    """Lambda function

    Parameters
    ----------
    event: dict, required

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    Response from DynamoDB put/update_item: dict
    """

    
    dynamodb = boto3.resource('dynamodb')
    table_name = os.environ['dynamoTableName']
    table = dynamodb.Table(table_name)


    
    # if a Reservation was created:
    if "CreateCapacityReservationResponse" in event['detail']['responseElements']:
        print("CREATE CapacityReservation Triggered!")

        event_results = event['detail']['responseElements']['CreateCapacityReservationResponse']['capacityReservation']

        item = {
            'capacityReservationId': event_results['capacityReservationId'],
            'startDate': event_results['startDate'],
            'user_arn': event['detail']['userIdentity']['arn'],
            'availabilityZone': event_results['availabilityZone'],
            'createDate': event_results['createDate'],
            'endDateType': event_results['endDateType'],
            'endDate': None,
            'ownerId': event_results['ownerId'],
            'capacityReservationArn': event_results['capacityReservationArn'],
            'totalInstanceCount': event_results['totalInstanceCount'],
            'instancePlatform': event_results['instancePlatform'],
            'ebsOptimized': event_results['ebsOptimized'],
            'tenancy': event_results['tenancy'],
            'instanceMatchCriteria': event_results['instanceMatchCriteria'],
            'availableInstanceCount': event_results['availableInstanceCount'],
            'instanceType': event_results['instanceType'],
            'ephemeralStorage': event_results['ephemeralStorage'],
            'state': event_results['state']
        }

        # if the reservation created ends at a 'Specific time', include the endDate attribute in the put_item operation
        if "endDate" in event_results:
            item['endDate'] = str(event_results['endDate'])

            print(item)

        response = table.put_item(
            Item=item
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response),
        }
    
        
    
    # if a Reservation was cancelled:
    if "CancelCapacityReservationResponse" in event['detail']['responseElements']:
        print("CANCEL CapacityReservation Triggered!")
        reservation_id = event['detail']['requestParameters']['CancelCapacityReservationRequest']['CapacityReservationId']
        cancel_date= event['detail']['eventTime']

        # update the item in DynamoDB. If no item exists, a new one will be created with the attributes specified in the update
        response = table.update_item(
            Key={
                'capacityReservationId': reservation_id
            },
            UpdateExpression="SET endDate = :dateVal",
            ExpressionAttributeValues={
                ':dateVal': cancel_date
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response),
        }

    return {
        "statusCode": 400,
        "body": "event parameter didn't match the requirements of the Lambda function code...",
    }
    
    

