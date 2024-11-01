import os
import boto3
import time
import requests
import json
from urllib.parse import urlparse, parse_qs




class SlackNotifier():
    sts = boto3.client("sts")
    account_id = sts.get_caller_identity()["Account"]
    slack_channel = os.environ['SLACK_CHANNEL']
    display_name = os.environ.get('SLACK_DISPLAY_NAME', 'CI/CD Alerts')
    display_icon = os.environ.get('SLACK_DISPLAY_ICON', ':incoming_envelope:')

    def __init__(self, region, pipeline_name, execution_id, commit_url, commit_message, commit_id, stage, action, state, category) -> None:
        self.webhook_url = os.environ['SLACK_WEBHOOK_URL']
        self.execution_link = f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline_name}/executions/{execution_id}/timeline?region={region}"
        self.pipeline_link = f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline_name}/view?region={region}"
        self.region = region
        self.pipeline_name = pipeline_name
        self.execution_id = execution_id
        self.commit_url = commit_url
        self.commit_message = commit_message
        self.commit_id = commit_id
        self.stage = stage
        self.action = action
        self.state = state
        self.category = category
        self.execution_summary = ''
        self.error_code = ''
        parsed_details = self._parse_repository_details(self.commit_url)
        self.repo_owner, self.repo = parsed_details if commit_url is not None else ('', '')


    def _parse_repository_details(self, commit_url):
        # Parse the URL
        parsed_url = urlparse(commit_url)
        # Extract query parameters
        query_params = parse_qs(parsed_url.query)
        # Extract the FullRepositoryId parameter
        full_repository_id = query_params.get('FullRepositoryId', [None])[0]
        if full_repository_id:
            owner_repo = full_repository_id.split('/')
            if len(owner_repo) == 2:
                return owner_repo[0], owner_repo[1]
        return None, None


    def send_failed_message(self, status_icon, color):
        commit_id_short = None
        if self.commit_id is not None:
            commit_id_short = self.commit_id[:7]

        if len(commit_message) > 120:
            commit_message = f"{commit_message[:119]}..."

        message = {
            "channel": self.slack_channel, # Override channel to send messages to
            "username": self.display_name, # Override display name
            "icon_emoji": self.display_icon,
            "attachments": [
                {
                    "fallback": f"{status_icon} *<{self.pipeline_link}|AWS CodePipeline | {self.region} | {self.account_id} >*", # Hyperlink
                    "pretext": f"{status_icon} *<{self.pipeline_link}|AWS CodePipeline | {self.pipeline_name} | {self.region} | {self.account_id} >*",
                    "color": color,
                    "fields": [
                        {
                            "title": f"Pipeline {self.category} Action {self.state}",
                            "value": f"Commit Message: _{self.commit_message}_\nCommit: <https://github.com/{self.repo_owner}/{self.repo}/commit/{self.commit_id}|*{commit_id_short}*>"
                        },
                        {
                            "title": f"Failure Reason: {self.error_code}",
                            "value": f"```\n{self.execution_summary}\n```"
                        },
                        {
                            "title": "Stage",
                            "value": self.stage,
                            "short": True
                        },
                        {
                            "title": "Action",
                            "value": self.action,
                            "short": True
                        }
                    ],
                    "footer": f"AWS CodePipeline | Execution: *<{self.execution_link}|{self.execution_id} >*",
                    "footer_icon": "https://a.slack-edge.com/production-standard-emoji-assets/13.0/google-medium/1f6a8.png", # You can replace this with the URL of your desired footer icon
                    "ts": time.time()
                }
            ]
        }


        response = requests.post(url=self.webhook_url, data=json.dumps(message))

    def send_message(self, status_icon, color):
        commit_id_short = None
        if self.commit_id is not None:
            commit_id_short = self.commit_id[:7]


        if len(commit_message) > 120:
            commit_message = f"{commit_message[:119]}..."
        
        message = {
            "channel": self.slack_channel, # Override channel to send messages to
            "username": self.display_name, # Override display name
            "icon_emoji": self.display_icon,
            "attachments": [
                {
                    "fallback": f"{status_icon} *<{self.pipeline_link}|AWS CodePipeline | {self.region} | {self.account_id} >*", # Hyperlink
                    "pretext": f"{status_icon} *<{self.pipeline_link}|AWS CodePipeline | {self.pipeline_name} | {self.region} | {self.account_id} >*",
                    "color": color,
                    "fields": [
                        {
                            "title": f"Pipeline {self.category} Action {self.state}",
                            "value": f"""
                                    Commit Message: _{self.commit_message}_\nCommit: <https://github.com/{self.repo_owner}/{self.repo}/commit/{self.commit_id}|*{commit_id_short}*>
                                """
                        },
                        {
                            "title": "Stage",
                            "value": self.stage,
                            "short": True
                        },
                        {
                            "title": "Action",
                            "value": self.action,
                            "short": True
                        }
                    ],
                    "footer": f"AWS CodePipeline | Execution: *<{self.execution_link}|{self.execution_id} >*",
                    "footer_icon": "https://a.slack-edge.com/production-standard-emoji-assets/13.0/google-medium/1f6a8.png", # You can replace this with the URL of your desired footer icon
                    "ts": time.time()
                }
            ]
        }
        response = requests.post(url=self.webhook_url, data=json.dumps(message))
        