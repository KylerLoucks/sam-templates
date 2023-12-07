import os
import boto3
import json
from notifier import SlackNotifier


client = boto3.client('codepipeline')

REGION = os.environ['AWS_REGION']

def handler(event, context):
    print(json.dumps(event))



    execution_id = event['detail']['execution-id']
    pipeline_name = event['detail']['pipeline']
    category = event['detail']['type']['category']
    state = event['detail']['state']

    response = client.get_pipeline_execution(
        pipelineName=pipeline_name,
        pipelineExecutionId=execution_id
    )

    artifact_revisions = response['pipelineExecution']['artifactRevisions']
    commit_id = artifact_revisions['revisionId']
    commit_url = artifact_revisions['revisionUrl']


    slack = SlackNotifier(
        REGION,
        pipeline_name,
        execution_id
    )







    
    if category == "Source":
        if state == "SUCCEEDED":
            pass
            # slack.send_started()
        elif state == "FAILED":
            pass
            # slack.send_failed()

    # if category == "Approval":
    #     if state == "STARTED":
    #         send_approval_needed()
    #     elif state == "SUCCEEDED":
    #         send_approved()
    #     elif state == "FAILED":
    #         send_approval_reject()
    
    # if category == "Build":
    #     if state == "STARTED"
    #         send_build_started()
    #     elif state == "SUCCEEDED":
    #         send_build_success()
    #     elif state == "FAILED":
    #         send_build_failed()
    
    # if category == "Deploy":
    #     if state == "STARTED":
    #         send_deploy_started()
    #     elif state == "SUCCEEDED":
    #         send_deploy_success()
    #     elif state == "FAILED":
    #         send_deploy_failed()