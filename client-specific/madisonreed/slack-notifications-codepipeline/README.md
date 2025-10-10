# Slack Notifications
This template defines a lambda function for sending CodePipeline updates to a slack channel via a Slack Webhook.

# Deploy

To prevent storing slack webhook url in the repo, deploy using parameter overrides

```zsh
sam build

sam deploy \
    --parameter-overrides \
        "pSlackWebhookUrl=<WEBHOOK-URL> \
        pSlackChannel=devops" \
    --stack-name ephemeral-pipeline-slack-alerts \
    --resolve-s3 \
    --capabilities CAPABILITY_NAMED_IAM \
    --on-failure DELETE
```