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


### CI/CD with ApiGateway

During the Build of the API Gateway the following steps should be ran:

1. Build the new lambda code version
```zsh
sam build
```

2. Deploy the code packages and any other IaC
```zsh
sam deploy
```

3. Publish a new Lambda version for each lambda function that is part of the API.
```zsh
LATEST_VERSION=$(aws lambda publish-version --function-name <function-name> --query 'Version' --output text)
```

4. Set a specific Lambda alias to point to the latest lambda version we just published, passing in the output from the previous (publish) command.
```zsh
aws lambda update-alias --function-name <function-name> --name <alias-name> --function-version $LATEST_VERSION
```


Final workflow example:
```zsh
sam build
sam deploy
LATEST_VERSION=$(aws lambda publish-version --function-name <function-name> --query 'Version' --output text)
aws lambda update-alias --function-name <function-name> --name dev --function-version $LATEST_VERSION
```