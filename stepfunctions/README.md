# Ephemeral Aurora Serverlss V2 Clusters
The templates described in this README will provide the ability to create ephemeral Aurora Clusters

# Usage

Deploy the `ephemeral-db-import.yml` Step Function template


Use the `aurora-serverless-v2.yml` template and pass in the `SnapshotIdentifier` for the snapshot that the Step Function template created.

This will create a net-new Aurora Serverless V2 Cluster with its password managed by Secrets Manager.

Now, you can create as many ephemeral Aurora Clusters as you want.

> [!Note]
> If you update the `aurora-serverless-v2` stack and make modifications to `SnapshotIdentifier` please be aware of the following:
> If you specify a property that is different from the previous `SnapshotIdentifier` restore property, a new DB cluster is restored from the specified `SnapshotIdentifier`, and the original DB cluster is deleted. 
> if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted.
> See the [AWS Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html) for more details.