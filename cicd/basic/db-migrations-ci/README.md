# Overview

Creates CodePipeline + CodeBuild inside the VPC for CodeBuild to be able to connect to RDS databases.

# Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- **AWS SAM CLI**: The AWS Serverless Application Model (SAM) CLI is a command-line tool for building, testing, and deploying serverless applications in AWS. You can download and install it from the [AWS SAM CLI installation page](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
- **AWS Credentials**: Properly configured AWS credentials are necessary to deploy resources. Make sure your AWS credentials are configured by following the [AWS CLI configuration instructions](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html).

## db-migrationsv2.yml

This template is used to deploy the CodePipeline + CodeBuild environment which is used to migrate Madison Reed's MySQL and MongoDB schemas.

### samconfig.toml

This file defines the configurations and parameters to pass for the CodePipeline infrastructure.

### Deploy

To deploy the infrastructure, use the following commands:

```bash
sam build -t db-migrationsv2.yml

# For the madisonreed-development account
sam deploy --config-env development

# For the madisonreed-staging account
sam deploy --config-env staging
```