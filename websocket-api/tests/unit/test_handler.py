import json

import pytest

from dynamoCRUDFunction import app


# run this unit test:
# python -m pytest tests/unit -v

@pytest.fixture()
def cloudtrail_event():
    """ Generates CloudTrail Create Reservation Event"""

    return {  
    "_comment": "--------------------- UNLIMITED Capacity Reservation Example (User Creates Reservation that has to be Manually Cancelled): -------------------------",

    "version": "0",
    "id": "bfaeac7f-a57f-ddc8-2058-2e2aa99fd13d",
    "detail-type": "AWS API Call via CloudTrail",
    "source": "aws.ec2",
    "account": "123456789012",
    "time": "2018-12-18T00:23:14Z",
    "region": "us-east-1",
    "resources": [],
    "detail": {
        "eventVersion": "1.08",
        "userIdentity": {
        "type": "AssumedRole",
        "principalId": "AROAYJS4TH7HKS36UETR4:kloucks",
        "arn": "arn:aws:sts::570351108046:assumed-role/cloud303-rnd/kloucks",
        "accountId": "ASIAYJS4TH7HHM4XNGEY",
        "accessKeyId": "ABCD123EFG",
        "sessionContext": {
            "sessionIssuer": {
                "type": "Role",
                "principalId": "AROAYJS4TH7HKS36UETR4",
                "arn": "arn:aws:iam::570351108046:role/cloud303-rnd",
                "accountId": "570351108046",
                "userName": "cloud303-rnd"
            },
            "webIdFederationData": {},
            "attributes": {
                "creationDate": "2023-01-29T00:49:58Z",
                "mfaAuthenticated": "false"
                }
            }
        },
        "eventTime": "2023-01-29T01:23:02Z",
        "eventSource": "ec2.amazonaws.com",
        "eventName": "CreateCapacityReservation",
        "awsRegion": "us-west-2",
        "sourceIPAddress": "50.39.190.67",
        "userAgent": "AWS Internal",
        "requestParameters": {
            "CreateCapacityReservationRequest": {
                "EndDateType": "unlimited",
                "Tenancy": "default",
                "InstanceCount": 1,
                "AvailabilityZone": "us-west-2a",
                "InstancePlatform": "Linux/UNIX",
                "EphemeralStorage": False,
                "InstanceMatchCriteria": "open",
                "InstanceType": "t2.micro",
                "EbsOptimized": False
            }
        },
        "responseElements": {
            "CreateCapacityReservationResponse": {
                "xmlns": "http://ec2.amazonaws.com/doc/2016-11-15/",
                "capacityReservation": {
                    "ephemeralStorage": False,
                    "ebsOptimized": False,
                    "instancePlatform": "Linux/UNIX",
                    "instanceType": "t2.micro",
                    "tenancy": "default",
                    "availableInstanceCount": 1,
                    "ownerId": 570351108046,
                    "totalInstanceCount": 1,
                    "availabilityZone": "us-west-2a",
                    "capacityReservationId": "cr-0c1589281e48747cf",
                    "endDateType": "unlimited",
                    "capacityReservationArn": "arn:aws:ec2:us-west-2:570351108046:capacity-reservation/cr-0c1589281e48747cf",
                    "state": "active",
                    "instanceMatchCriteria": "open",
                    "startDate": "2023-01-29T01:23:02.000Z",
                    "createDate": "2023-01-29T01:23:02.000Z"
                },
                "requestId": "a82d13bc-f845-4e85-98b1-d6bc22783e00"
            }
        },
        "requestID": "a82d13bc-f845-4e85-98b1-d6bc22783e00",
        "eventID": "a88f9033-fcea-4f7d-95da-4b291b90e6dd",
        "readOnly": False,
        "eventType": "AwsApiCall",
        "managementEvent": True,
        "recipientAccountId": "570351108046",
        "eventCategory": "Management",
        "sessionCredentialFromConsole": "true"
    }
}




def test_lambda_handler(cloudtrail_event):

    ret = app.lambda_handler(cloudtrail_event, "")
    
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"
