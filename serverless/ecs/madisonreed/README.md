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
sam deploy -t ecs/madisonreed-ecs-tester.yml \
  --resolve-s3 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    "pAppName=pr1 \
     pVpcId=vpc-09ef4a53e9290ca17 \
     pPrivateSubnetId1=subnet-01086857935bfcf34 \ 
     pPrivateSubnetId2=subnet-056e57e04fea05dd5 \
     pPublicSubnetId1=subnet-0598f465e77230bd5 \
     pPublicSubnetId2=subnet-0d650820a97fa5ba3 \
     pR53HostedZoneId=Z0323068C9DQS081P13G \
     pWebsiteEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/websitetest-pr16692@sha256:d4583ba1ae7255ec693640b787819710a10297730517c0edfacba43a94e70def \
     pACMCertificateArn=arn:aws:acm:us-east-1:174743933558:certificate/07f48ca4-3dcf-4ed7-b4df-147b3412be62" \
     pColorAdvisorApiUrl=test \
  --stack-name pr1-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
  --no-confirm-changeset \
  --on-failure DELETE
```


### Update ECS service when a change is made:

```bash
aws ecs update-service --cluster pr1-cluster --service pr1-frontend --force-new-deployment
```


### Cleanup
```bash
# Sam delete waits until the stack is fully deleted before moving to the next line. To use async deletion, try cloudformation
sam delete --stack-name pr1-ephemeral --no-prompts
sam delete --stack-name pr1-ecr --no-prompts


aws cloudformation delete-stack --stack-name pr1-ephemeral
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
aws codepipeline start-pipeline-execution --name ${PR_ID}-pipeline --variables name=PR_ID,value=123 name=PR_EVENT,value=closed
```




# Deploy nested stacks
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




# INFORMATIONAL
#### Notable files to be aware of:
* **.github/workflows/ephemeral-envs.yml** - Github Action for deploying CodePipeline ephemeral deployment pipeline.
* **ephemeralenv/** - contains IaC and buildspec code for Ephemeral environments.
* **ephemeralenv/pipeline.yml** - Github Action uses SAM CLI to deploy this stack when a PR is made into a branch that contains the `ephemeral-envs.yml` github action config and the branch matches the criteria needed to trigger the workflow.

* **ephemeralenv/root.yml** - Nested Stack template used to link dependency of API and ECS child stacks, while also improving maintainability for the SAM Application.
* **ephemeralenv/ecs/** - Contains child template configuration for CodeBuild to deploy ECS components.
* **ephemeralenv/api/** - Contains child template configuration for CodeBuild to deploy Color Advisor API components.