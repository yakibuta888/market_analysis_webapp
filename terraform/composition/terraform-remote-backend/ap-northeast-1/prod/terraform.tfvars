########################################
# Environment setting
########################################
region           = "ap-northeast-1"
role_name        = "Admin"
profile_name     = "masanori"
env              = "prod"
application_name = "market-analysis-webapp"
app_name         = "market-analysis-webapp"

########################################
## Terraform State S3 Bucket
########################################
acl                = "private"
force_destroy      = false
object_lock_enabled = false
versioning_enabled = true
object_ownership = "BucketOwnerEnforced"

## s3 bucket public access block ##
block_public_policy     = true
block_public_acls       = true
ignore_public_acls      = true
restrict_public_buckets = true

########################################
## DynamoDB
########################################
read_capacity  = 5
write_capacity = 5
hash_key       = "LockID" # state locking
sse_enabled    = true     # enable server side encryption
attribute_name = "LockID"
attribute_type = "S"
