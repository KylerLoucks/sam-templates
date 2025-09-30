# SOC2 Conformance Pack for AWS Organizations

This guide demonstrates how to deploy an organization-wide SOC2 control conformance pack using AWS Config.

## Prerequisites

Before deploying this conformance pack, ensure that AWS Config is properly enabled in your Audit account. This is typically accomplished through AWS Control Tower, which automatically sets up AWS Config with the necessary configurations for organization-wide compliance monitoring.

**Required Setup:**
- AWS Control Tower deployed in your organization
- AWS Config enabled in the Audit account (automatically configured by Control Tower)
- Appropriate cross-account roles for Config access (handled by Control Tower)
- S3 bucket in the Audit account to store the conformance pack template

If you haven't deployed Control Tower or need to manually configure AWS Config, you'll need to set up Config recording and delivery channels in your Audit account before proceeding.

### S3 Bucket Setup

Create an S3 bucket in your Audit account and upload the conformance pack template:

```bash
# Switch to the Audit account
# Create an S3 bucket for storing conformance pack templates
BUCKET_NAME="your-audit-account-config-templates"
REGION="us-east-1"  # Use your preferred region

aws s3 mb s3://$BUCKET_NAME --region $REGION

# Upload the SOC2 conformance pack template
aws s3 cp soc2-aws-config-conformance-pack.yml s3://$BUCKET_NAME/conformance-packs/

# Verify the upload
aws s3 ls s3://$BUCKET_NAME/conformance-packs/
```

**Note:** The S3 bucket must be in the same region where you plan to deploy the organization conformance pack.

## Deployment Steps

Assume a role in the management account where Control Tower was enabled and deployed.

```bash
# 1) Enable AWS Config organization-wide access (both service principals are required)
aws organizations enable-aws-service-access --service-principal config.amazonaws.com
aws organizations enable-aws-service-access --service-principal config-multiaccountsetup.amazonaws.com

# 2) Register your Audit account as the delegated administrator for AWS Config
AUDIT_ACCOUNT_ID=123456789012
aws organizations register-delegated-administrator --account-id $AUDIT_ACCOUNT_ID --service-principal config.amazonaws.com
aws organizations register-delegated-administrator --account-id $AUDIT_ACCOUNT_ID --service-principal config-multiaccountsetup.amazonaws.com

# 3) (Optional) Verify the delegated administrator registration
aws organizations list-delegated-administrators --service-principal config.amazonaws.com
```

Deploy the [org-soc-2-conformance-pack-deployment.yml](org-soc-2-conformance-pack-deployment.yml) CloudFormation template to the Audit account in all regions where you want organization-wide compliance monitoring.

```bash
# Deploy the organization conformance pack (run this in the Audit account)
BUCKET_NAME="your-audit-account-config-templates"
REGION="us-east-1"  # Use the same region as your S3 bucket

aws cloudformation deploy \
  --template-file org-soc-2-conformance-pack-deployment.yml \
  --stack-name org-soc2-conformance-pack \
  --parameter-overrides pTemplateS3Uri=s3://$BUCKET_NAME/conformance-packs/soc2-aws-config-conformance-pack.yml \
  --region $REGION \
  --capabilities CAPABILITY_IAM
```

**Important:** 
- The conformance pack will only monitor resources in the region where it's deployed
- The S3 bucket and CloudFormation stack must be in the same region
- For example, deploying in `us-east-1` will evaluate SOC2 compliance for resources in `us-east-1` across all organization accounts, but not in other regions
- Deploy to multiple regions as needed for comprehensive coverage
- Make sure to update the `pTemplateS3Uri` parameter with your actual bucket name
