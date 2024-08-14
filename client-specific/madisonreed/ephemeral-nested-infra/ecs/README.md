# Deploy ecs-network-tester-private-ServiceConnect.yml
> [!NOTE] 
You must be connected to VPN (OpenVPN deployed via EC2 works) to be able to access private IP address of deployed ECS services.

### ECS Connection Tester Deploy
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


### MadisonReed services deploy

```bash
sam build -t madisonreed-ServiceConnect.yml    
```

***sam deploy parameters subject to change***
```bash
sam deploy -t madisonreed-ServiceConnect.yml \
  --resolve-s3 \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameter-overrides \
     pAppName=pr1 \
     pVpcId=vpc-09ef4a53e9290ca17 \
     pPrivateSubnetId1=subnet-01086857935bfcf34 \
     pPrivateSubnetId2=subnet-056e57e04fea05dd5 \
     pWebsiteEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/website:latest \
     pTophatEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/tophat:latest \
     pSocketIoEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/tophat:latest \
     pApiServerEcrImageUri=174743933558.dkr.ecr.us-east-1.amazonaws.com/apiserver:latest \
  --stack-name pr1-ephemeral \
  --tags CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
  --no-confirm-changeset \
  --on-failure DELETE
```