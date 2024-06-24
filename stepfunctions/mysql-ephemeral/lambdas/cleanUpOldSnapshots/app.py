
import boto3
import os
import json

ec2 = boto3.client('ec2')

# Amount of snapshots to retain
SNAPSHOT_RETAIN_AMOUNT = int(os.environ['SNAPSHOT_RETAIN_AMOUNT'])

def lambda_handler(event, context):
    
    # Get all snapshots with ephemeral-mysql tag key
    snapshots: list = ec2.describe_snapshots(
        Filters=[
            {
                'Name': 'tag-key',
                'Values': ['ephemeral-mysql']
            }
        ]
    )['Snapshots']

    # Sort snapshots by start time in descending order
    snapshots.sort(key=lambda x: x['StartTime'], reverse=True)

    print(f"Sorted the following snapshots: {snapshots}")

    # Get snapshots to delete (all except the amount specified)
    snapshots_to_delete = snapshots[SNAPSHOT_RETAIN_AMOUNT:]

    for snapshot in snapshots_to_delete:
        snapshot_id = snapshot['SnapshotId']
        print(f"Deleting snapshot {snapshot_id}")
        ec2.delete_snapshot(SnapshotId=snapshot_id)

    return {
        'statusCode': 200,
        'body': f"Deleted {len(snapshots_to_delete)} snapshots"
    }