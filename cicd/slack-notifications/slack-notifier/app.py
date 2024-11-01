import os
import boto3
import json
from notifier import SlackNotifier


client = boto3.client('codepipeline')

REGION = os.environ['AWS_REGION']

SOURCE_ICON = os.environ.get('SOURCE_ICON', ':pushpin:')
APPROVAL_ICON = os.environ.get('APPROVAL_ICON', ':spiral_note_pad:')
BUILD_ICON = os.environ.get('BUILD_ICON', ':hammer_and_wrench:')
DEPLOY_ICON = os.environ.get('DEPLOY_ICON', ':rocket:')

def handler(event, context):
    print(json.dumps(event))



    execution_id = event['detail']['execution-id']
    pipeline_name = event['detail']['pipeline']
    category = event['detail']['type']['category']
    state = event['detail']['state']
    stage = event['detail']['stage']
    action = event['detail']['action']



    response = client.get_pipeline_execution(
        pipelineName=pipeline_name,
        pipelineExecutionId=execution_id
    )

    print(f"Pipeline Execution {json.dumps(response)}")

    commit_message = None
    commit_id = None
    commit_url = None


    # Revision summary isn't included until the Source stage Succeeds
    artifact_revisions = response['pipelineExecution']['artifactRevisions']
    if len(artifact_revisions) > 0:
        revision_summary_str = artifact_revisions[0]['revisionSummary']
        revision_summary = json.loads(revision_summary_str)
        commit_message = revision_summary['CommitMessage']
        commit_id = artifact_revisions[0]['revisionId']
        commit_url = artifact_revisions[0]['revisionUrl']


    slack = SlackNotifier(
        REGION,
        pipeline_name,
        execution_id,
        commit_url,
        commit_message,
        commit_id,
        stage,
        action,
        state,
        category
    )

    
    if category == "Source":
        if state == "SUCCEEDED":
            slack.send_message(status_icon=SOURCE_ICON, color="#34bb13")
        elif state == "FAILED":
            slack.execution_summary = event['detail']['execution-result']['external-execution-summary']
            slack.error_code = event['detail']['execution-result']['error-code']
            
            slack.send_failed_message(status_icon=":x:", color="#D00000")


    if category == "Approval":
        if state == "STARTED":
            slack.send_message(status_icon=APPROVAL_ICON, color="#34bb13")
        elif state == "SUCCEEDED":
            slack.send_message(status_icon=APPROVAL_ICON, color="#34bb13")
        elif state == "FAILED":
            slack.execution_summary = event['detail']['execution-result']['external-execution-summary']
            slack.error_code = event['detail']['execution-result']['error-code']
            slack.send_failed_message(status_icon=":x:", color="#D00000")
    
    if category == "Build":
        if state == "STARTED":
            slack.send_message(status_icon=BUILD_ICON, color="#34bb13")
        elif state == "SUCCEEDED":
            slack.send_message(status_icon=BUILD_ICON, color="#34bb13")
        elif state == "FAILED":
            slack.execution_summary = event['detail']['execution-result']['external-execution-summary']
            slack.error_code = event['detail']['execution-result']['error-code']
            
            slack.send_failed_message(status_icon=":x:", color="#D00000")
    
    if category == "Deploy":
        if state == "STARTED":
            slack.send_message(status_icon=DEPLOY_ICON, color="#34bb13")
        elif state == "SUCCEEDED":
            slack.send_message(status_icon=DEPLOY_ICON, color="#34bb13")
        elif state == "FAILED":
            slack.execution_summary = event['detail']['execution-result']['external-execution-summary']
            slack.error_code = event['detail']['execution-result']['error-code']
            
            slack.send_failed_message(status_icon=":x:", color="#D00000")