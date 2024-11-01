# MySQL Docker container with baked-in SQL dump


## Dockerfile-mysql

This docker file uses a multi-stage build to bake-in the MySQL dump within the container.
This maintains one of dockers most key benifits of having fast initalization of the environment. Biggest downside and limitation is ECRs 50GB image size maximum. ECR pushes are compressed, so SQL dumps of 160GB can work, but anything larger will be an issue for ECS fargates 200gb ephemeral storage limit.

## create_dbs.sh
This file is used during the docker build of `Dockerfile-mysql`.

It is used to ensure the correct MySQL database(s) are created before the dump file is ran against the database(s).