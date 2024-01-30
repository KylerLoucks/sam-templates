# Deployment order

### Deploy ECR repos

```bash
sam build -t ecr.yml
```


```bash
sam deploy -t ecr.yml --config-env ecr --parameter-overrides "pAppName=pr1" --stack-name pr1-ecr --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') --no-confirm-changeset
```


### Build and push Docker Images to the ECR repos

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 174743933558.dkr.ecr.us-east-1.amazonaws.com 
```

```bash
docker build -f docker-flask-frontend/Dockerfile -t 174743933558.dkr.ecr.us-east-1.amazonaws.com/website-pr1:latest ./docker-flask-frontend/  
```

```bash
docker push 174743933558.dkr.ecr.us-east-1.amazonaws.com/website-pr1:latest
```


### Deploy Main Infra

```bash
sam build -t madisonreed-ephemeral-tester.yml
```


```bash
sam deploy -t madisonreed-ephemeral-tester.yml \
  --config-env ephemeral \
  --parameter-overrides \
    "pAppName=pr1 \
     pVpcId=vpc-09ef4a53e9290ca17 \
     pPrivateSubnetIds=subnet-01086857935bfcf34,subnet-056e57e04fea05dd5 \
     pPublicSubnetIds=subnet-0598f465e77230bd5,subnet-0d650820a97fa5ba3 \
     pR53HostedZoneId=Z0323068C9DQS081P13G \
     pACMCertificateArn=arn:aws:acm:us-east-1:174743933558:certificate/07f48ca4-3dcf-4ed7-b4df-147b3412be62" \
  --stack-name pr1-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
  --no-confirm-changeset
```


### Update ECS service when a change is made:

```bash
aws ecs update-service --cluster pr1-cluster --service pr1-frontend --force-new-deployment
```


### Cleanup
```bash
sam delete --stack-name pr1-ephemeral --no-prompts
sam delete --stack-name pr1-ecr --no-prompts
```


# Start Codepipeline, passing variables from Github Actions:
```bash
aws codepipeline start-pipeline-execution --name ephemeral-pipeline --variables name=PR_ID,value=123 name=COMMIT_ID,value=idefg name=PR_EVENT,value=opened
```