import os

MESSAGE_TEMPLATE = {
        "channel": "<#notification-slack-channel>",
        "username": "<slack-bot-name>",
        "icon_emoji": ":uh-oh-sooj:",
        "attachments": [
            {
                "fallback": "CICD: <https://google.com/|open link here>", # Hyperlink
                "pretext": "CICD: <https://google.com/|open link here>",
                "color": "#34bb13",
                "fields": [
                    {
                        "title": "Server",
                        "value": "server is starting!!"
                    }
                ]
            }
        ]
    }

execution_link = """

"""

class SlackNotifier():

    def __init__(self, region, pipeline_name, execution_id) -> None:
        self.webhook_url = os.environ['SLACK_WEBHOOK_URL']
        self.execution_link = f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline_name}/executions/{execution_id}/timeline?region={region}"
        self.pipeline_link = f"https://{region}.console.aws.amazon.com/codesuite/codepipeline/pipelines/{pipeline_name}/view?region={region}"

