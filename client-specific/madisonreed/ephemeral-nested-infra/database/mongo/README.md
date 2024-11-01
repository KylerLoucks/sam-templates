# Mongo Docker container with baked-in dump file(s)


## Dockerfile-mongo

This docker file uses a multi-stage build to bake-in the Mongo dump file(s) within the container.

## mongoimport.sh
This script is used during the docker build of `Dockerfile-mongo` to restore the mongo dump file(s) into the container.

