# ECS network tester


## Build tester docker image

### Build and push Docker Images to the ECR repos
> [!NOTE] 
Requires deployment of an ecr repo called `ecs-tester`
Replace `<ACCOUNT_ID>` with the value of your AWS Account ID


```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com 
```

```bash
docker build -f docker-flask-frontend/Dockerfile -t <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ecs-tester:latest ./docker-flask-frontend/  
```

```bash
docker push <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com/ecs-tester:latest
```

## Deploy ECS Connection Tester Deploy (Service Connect)
> [!NOTE] 
You must be connected to VPN (OpenVPN deployed via EC2 works) to be able to access private IP address of deployed ECS services.
This is due to the fact that Service Connect is done through the private VPC network. An ALB would be required to access the public service without a VPN.

To build and deploy the Service Connect version, run the following commands:


```
sam build -t ecs-network-tester-private-ServiceConnect.yml
```

```
sam deploy -t ecs-network-tester-private-ServiceConnect.yml \
  --resolve-s3 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    "pAppName=pr1 \
     pVpcId=vpc-09ef4a53e9290ca17 \
     pPrivateSubnetId1=subnet-01086857935bfcf34 \
     pPrivateSubnetId2=subnet-056e57e04fea05dd5 \
     pWebsiteEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/connectiontest:latest" \
  --stack-name pr1-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
  --no-confirm-changeset \
  --on-failure DELETE
```

## Deploy ECS Connection Tester Deploy (Public ALB)
To build and deploy the ALB version of the ECS tester, run the following commands:

```
sam build -t ecs-tester-public-ALB.yml
```

```
sam deploy -t ecs-tester-public-ALB.yml \
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
     pWebsiteEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/connectiontest:latest" \
  --stack-name pr1-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
  --no-confirm-changeset \
  --on-failure DELETE
```