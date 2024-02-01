# Multi-Domain REST API

Creates an API gateway REST API that uses stage variables to deploy a certain lambda alias a Stage (deployment) of the API



### Deploy
```
sam deploy -t template.yml \
  --config-env ephemeral \
  --parameter-overrides \
    "pAppName=pr1 \
     pACMCertificateArn=arn:aws:acm:us-east-1:174743933558:certificate/07f48ca4-3dcf-4ed7-b4df-147b3412be62" \
  --stack-name pr1-color-advisor-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
  --no-confirm-changeset
```