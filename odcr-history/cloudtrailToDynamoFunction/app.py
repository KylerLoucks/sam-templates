import json
import cfnresponse
import boto3
import logging
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)

cloudtrail = boto3.client("cloudtrail")
dynamodb = boto3.resource("dynamodb")

def lambda_handler(event, context):
    """Lambda function

    Parameters
    ----------
    event: dict, required

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html
    """
    try:
        logger.info("Received event: %s" % json.dumps(event))

        # grab dynamodb table from template.yaml
        table = dynamodb.Table(event['ResourceProperties']['DynamoDBTableName'])

        create_events = get_all_events_by_name("CreateCapacityReservation")
        cancel_events = get_all_events_by_name("CancelCapacityReservation")

        # Create a new list, called history, that has the combined create and cancel info
        history = []
        for create_event in create_events:
            # Check if the create event actually resulted in a OCDR. If not, do nothing.
            if "errorMessage" in create_event:
                continue

            # Get the portion of the create event that contains the info we want
            create_info = create_event["responseElements"][
                "CreateCapacityReservationResponse"
            ]["capacityReservation"]

            
                

            # Get the cancel date using the cancel event associated with this capacity
            # reservation ID
            cancel_date = get_odcr_cancel_date(
                create_info["capacityReservationId"], cancel_events
            )

            # Combine all of the info we want into a single dictionary
            ocdr_info = {
                "user_arn": create_event["userIdentity"]["arn"],
                **create_info
            }

            # If the reservation created wasn't a 'limited' endDateType, set the endDate to the time it was cancelled
            if "endDate" not in create_info:
                ocdr_info["endDate"] = cancel_date

            # Add it to our history list
            history.append(ocdr_info)
        
            # Batch write the items from the 'history' list to DynamoDB
            with table.batch_writer() as batch:
                for item in history:
                    batch.put_item(Item=item)
                    # print(f"Put item in database: \n {item}")
            result = cfnresponse.SUCCESS
    except ClientError as e:
        logger.error('Error: %s', e)
        result = cfnresponse.FAILED
    
    # send the success or failed response back to cloudformation
    cfnresponse.send(event, context, result, {})



def get_all_events_by_name(event_name):
    """Gets all of the CloudTrail event payloads by EventName"""

    # args must be the same with each call to lookup_events, so just define it once
    # and reuse with each call
    lookup_events_kwargs = {
        "LookupAttributes": [
            {
                "AttributeKey": "EventName",
                "AttributeValue": event_name,
            },
        ],
        "MaxResults": 50,
    }

    # Get first page of results
    response = cloudtrail.lookup_events(**lookup_events_kwargs)
    events = response["Events"]

    # While there are more results, continue to fetch them and add to events list
    while "NextToken" in response:
        response = cloudtrail.lookup_events(
            **lookup_events_kwargs, NextToken=response["NextToken"]
        )
        events += response["Events"]

    cloudtrail_events = [json.loads(e["CloudTrailEvent"]) for e in events]

    return cloudtrail_events


def get_odcr_cancel_date(capacity_reservation_id, cancel_events):
    """Gets the time that the OCDR was cancelled using the cancel events we found in
    CloudTrail"""

    # Filter out the unnsuccessful cancel events
    successful_cancel_events = [
        e
        for e in cancel_events
        if e["responseElements"]
        and (
            e["responseElements"]["CancelCapacityReservationResponse"]["return"] is True
        )
    ]

    # Find the cancel events that have the capacity reservation id we're looking for
    cancel_event_matches = [
        e
        for e in successful_cancel_events
        if e["requestParameters"]["CancelCapacityReservationRequest"][
            "CapacityReservationId"
        ]
        == capacity_reservation_id
    ]

    if len(cancel_event_matches) == 0:
        # No cancel event found. The OCDR is still running, and hasn't been cancelled
        # yet
        return None
    elif len(cancel_event_matches) > 1:
        # This should never happen. Let's fail the script so we can investigate
        raise RuntimeError(
            f"Multiple cancel events found for {capacity_reservation_id}"
        )
    else:
        # Return the event time of the matching event
        return cancel_event_matches[0]["eventTime"]
    
    

