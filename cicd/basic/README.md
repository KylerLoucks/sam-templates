


# Deploy build-ci.yml example


```
sam deploy -t build-ci.yml \
    --stack-name build-test \
    --resolve-s3 \
    --capabilities CAPABILITY_NAMED_IAM \
    --parameter-overrides \
        pRepoOwner=MadisonReed \
        pRepoName=mr \
        pCodestarConnectionArn=arn:aws:codestar-connections:us-east-1:174743933558:connection/d27c0b2b-88c2-45ac-b8f4-89b0e04af6fd \
        pTriggerBranch=c303/ephemeral/main \
        pCodeBuildComputeType=BUILD_GENERAL1_MEDIUM \
        pBuildSpecPath=buildspec-buildlambdafunctionsv3.yml
```