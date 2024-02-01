# Deployment order (CodePipeline CodeBuild, not for Standalone CodeBuild)

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







# Standalone CodeBuild (Triggered by Github Actions)


### Deploy CodePipeline, CodeBuild template.
Variables are pulled from build project environment vars

```bash
sam build -t pipeline.yml
```


```bash
sam deploy -t pipeline.yml --config-env pipeline --parameter-overrides "pAppName=${PR_ID}" --stack-name pr1-pipeline --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') --no-confirm-changeset
```

###  Start Codepipeline, passing variables from Github Actions:
```bash
aws codepipeline start-pipeline-execution --name ${PR_ID}-pipeline --variables name=PR_ID,value=123 name=COMMIT_ID,value=idefg name=PR_EVENT,value=opened
```




# TESET
sam deploy -t root.yml \
  --config-env ephemeral \
  --parameter-overrides \
    "pAppName=pr1 \
     pVpcId=vpc-09ef4a53e9290ca17 \
     pPrivateSubnetId1=subnet-01086857935bfcf34 \ 
     pPrivateSubnetId2=subnet-056e57e04fea05dd5 \
     pPublicSubnetId1=subnet-0598f465e77230bd5 \
     pPublicSubnetId2=subnet-0d650820a97fa5ba3 \
     pR53HostedZoneId=Z0323068C9DQS081P13G, \
     pACMCertificateArn=arn:aws:acm:us-east-1:174743933558:certificate/07f48ca4-3dcf-4ed7-b4df-147b3412be62" \
  --stack-name pr1-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ')