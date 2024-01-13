# Deployment order

### Deploy ECR repos

```bash
sam build -t ecr.yml
```


```bash
sam deploy -t ecr.yml --config-env ecr --parameter-overrides "pAppName=pr1" --stack-name pr1-ecr --no-confirm-changeset
```


### Build and push Docker Images to the ECR repos

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 570351108046.dkr.ecr.us-east-1.amazonaws.com 
```

```bash
docker build -f Dockerfile.frontend -t 570351108046.dkr.ecr.us-east-1.amazonaws.com/pr1-frontend:latest .  
```

```bash
docker push 570351108046.dkr.ecr.us-east-1.amazonaws.com/pr1-frontend:latest
```


### Deploy Main Infra

```bash
sam build -t template.yml
```


```bash
sam deploy -t template.yml --config-env ephemeral --parameter-overrides "pAppName=pr1 pVpcId=vpc-094590ab31d2c639f pPrivateSubnetIds=subnet-050fa317f4ea060dd,subnet-08c6fecb378269d0b" --stack-name pr1-ephemeral --no-confirm-changeset
```


### Update ECS service when a change is made:

```bash
aws ecs update-service --cluster pr1-cluster --service pr1-frontend --force-new-deployment
```


### Cleanup
```bash
sam delete --stack-name pr1-ephemeral --no-prompts
```