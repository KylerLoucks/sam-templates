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

# Potential/Known Issues & Debugging
The EBS volumes (root & database data) have a fixed size. If either of these get full, the state machine will fail.

## CloudWatch Logs
You can check for errors and if the size is getting close to full in the `/aws/ssm/SfnRunCommandByInstanceIds` CloudWatch log group.
The log stream corresponds to the EC2 instanceId that the script ran on. There will be two streams, one for the `stderr` and `stdout`. 

You can find the InstanceId by following these steps:
1. Open `Step Functions` console and open the import State Machine in question (MySQL/Mongo).
2. Select the execution you want to look into.
3. Select the `RunInstances` step in the `Graph View` tree.
4. On the right-hand side, look through the `Task result` JSON output for the `InstanceId` key and value.

Here is an example of the size message at the end of the script:
```
Database mounted EBS Volume disk space:
Filesystem      Size  Used Avail Use% Mounted on
/dev/nvme1n1     49G   21G   26G  45% /data/db
Root Volume disk space:
Filesystem      Size  Used Avail Use% Mounted on
/dev/root        60G   18G   42G  30% /
Script completed.
```