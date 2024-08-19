# Ephemeral Mongo EBS volume

Connect to the EC2 instance from local:
```zsh
mongosh "mongodb://<ec2-instance-private-ip>:27017"
```

Show databases:
```zsh
show dbs
```


# Deploying

```zsh
sam build -t ephemeral-db-mongo-ebs.yml
```

```zsh
sam deploy -t ephemeral-db-mongo-ebs.yml \
    --resolve-s3 \
    --capabilities CAPABILITY_NAMED_IAM \
    --confirm-changeset \
    --stack-name MongoEphemeralSnapshotStateMachine
```