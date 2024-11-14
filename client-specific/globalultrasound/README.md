# About
These templates were used to deploy Wordpress, Orthanc, and Laravel (Backend API) to ECS.

The templates use cross-stack references to have separation of concerns between stateful and stateless and networking resources.


## Deployment order (stateful then stateless):
1. aurora-mysql-serverless.yml
2. efs.yml
3. cluster.yml
4. alb.yml
5. laravel-svc.yml
6. orthanc-svc.yml
7. wordpress-svc.yml

### NOTE
TaskDefinition is split out into its own stack to avoid issues when trying to update it to include more environment variables.

This is because CODE_DEPLOY deployment controller doesn't allow updates to ECS Services and it must be updated from the CodeDeploy Pipeline instead.