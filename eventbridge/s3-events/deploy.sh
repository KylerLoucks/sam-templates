#!bin/bash
sam deploy -t template.yml \
    --resolve-s3 \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        pBucketName=pr16899-pipeline-artifacts-174743933558-us-east-1 \
    --stack-name bucket-test \
    --tags \
        CleanupDate=$(date -u -d "+10 days" '+%Y-%m-%dT%H:%M:%SZ') \
        costallocationtag:test=pr16899 \
    --no-confirm-changeset \
    --on-failure DELETE