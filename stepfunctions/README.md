# Ephemeral Aurora Serverlss V2 Clusters
The templates described in this README will provide the ability to create ephemeral Aurora Clusters

# Usage

Deploy the `ephemeral-db-import.yml` Step Function template


Use the `aurora-serverless-v2.yml` template and pass in the `SnapshotIdentifier` for the snapshot that the Step Function creates after a successful run.

This will create a net-new Aurora Serverless V2 Cluster with its password managed by Secrets Manager.

Now, you can create as many ephemeral Aurora Clusters as you want.

> [!Note]
> If you update the `aurora-serverless-v2` stack and make modifications to `SnapshotIdentifier` please be aware of the following:
> If you specify a property that is different from the previous `SnapshotIdentifier` restore property, a new DB cluster is restored from the specified `SnapshotIdentifier`, and the original DB cluster is deleted. 
> if you don't specify the SnapshotIdentifier property, an empty DB cluster is created, and the original DB cluster is deleted.
> See the [AWS Documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html) for more details.



# Notables

1. The `ephemeral-db-import.yml` stack currently is hardcoded to use MySQL 8.0 and a database dump bucket.
> These values will need to be changed accordingly. Before the import script, the aurora db also has the following databases created: `tophat magento inventory`

2. Both templates use the `ManageMasterUserPassword` flag, which uses Secrets Manager to manage the database credentials. This allows us to have a rotatable password that we don't have to manage.
> When you restore a snapshot with this flag, it no longer uses the password tied to the snapshot at the time of creation. Now, it will use Secrets Manager to have a new, rotatable password.