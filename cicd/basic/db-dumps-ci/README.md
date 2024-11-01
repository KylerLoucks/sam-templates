# Ephemeral Development environment SAM templates
Contains SAM templates used for testing ephemeral environments

## db-ci.yml

This file is used to deploy the CodeBuild environment which will build new versions of MadisonReed's MySQL and Mongo dumps stored in S3 and push them to ECR.

The ECR repository is included in the template, so deploying this separately isn't required.


### Deploy
```bash
sam build

# mysql
sam deploy --config-env mysql

# mongo
sam deploy --config-env mongo
```