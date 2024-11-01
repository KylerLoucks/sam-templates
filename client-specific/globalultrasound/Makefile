STACK_NAME := wordpress-ecs-svc
TEMPLATE_FILE := wordpress.yaml
REGION := us-east-1

# CloudFormation Parameters
PARAMETERS := \
    DBUsername=master \
    pAlbStackName=cluster-alb-gusi \
    pClusterStackName=gusi-cluster \
    pCPU=256 \
    pEcrRepo=gusi-wordpress \
    pImageVersion=latest \
    pMemory=512 \
    pMySQLDBStackName=wordpress-aurora-mysql \
    pSubnetIds=subnet-0e9946d826ebbb7a6,subnet-096cfcd34b9e5eecb \
    pVpcId=vpc-0c831f0bf67f01743

.PHONY: deploy
deploy:
	aws cloudformation deploy \
    	--template-file $(TEMPLATE_FILE) \
        --stack-name $(STACK_NAME) \
        --region $(REGION) \
        --capabilities CAPABILITY_NAMED_IAM \
        --parameter-overrides $(PARAMETERS)