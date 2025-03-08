This folder contains all IaC for playopulence.com <3

* CodePipeline.yml - Deploys a pipeline that uses CodeDeploy EC2/On-Premises to deploy our Source code to tagged EC2 Instances.
* appspec.yml - contains info on how our source files are copied and the scripts that are ran throughout the deploy process.
* EC2_PROD_Weboscket_Cloudflare.yaml - Deploys our standalone EC2 instance that runs Opulence websocket backend and other backend AWS resources used for Opulence.