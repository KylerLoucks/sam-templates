# Description
This template will deploy a custom docker image lambda. 

when `sam deploy` is called, it will automatically run the needed commands to build and push the docker image to the ECR repo specified in the `samconfig.toml`



## Create ECR repo
Create an ECR repo and reference it in the `samconfig.toml`