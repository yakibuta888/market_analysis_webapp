# Terraform Remote Backendに必要なリソースを3-layered Module Architectureで作成

Project architecture:
```sh
.
├── README.md
├── composition
│   └── terraform-remote-backend # <--- Step 3: Create Composition layer and define all the required inputs to Infrastructure module's main.tf
│       └── ap-northeast-1 
│           └── prod      
│               ├── data.tf
│               ├── main.tf # <----- this is the entry point
│               ├── outputs.tf
│               ├── providers.tf
│               ├── terraform.tfstate
│               ├── terraform.tfstate.backup
│               ├── terraform.tfvars
│               └── variables.tf
├── infrastructure_modules # <---- Step 2: Create Infrastructure Modules (abstraction layer using Facade design pattern) and consume resource modules
│   └── terraform_remote_backend
│       ├── data.tf
│       ├── main.tf
│       ├── outputs.tf
│       └── variables.tf
└── resource_modules  # <----- Step 1: Replicate remote TF modules in local Resource Modules
    ├── database
    │   └── dynamodb
    │       ├── main.tf
    │       ├── outputs.tf
    │       └── variables.tf
    ├── identity
    │   └── kms_key
    │       ├── main.tf
    │       ├── outputs.tf
    │       └── variables.tf
    └── storage
        └── s3    # <---- replicated locally from remote TF module: https://github.com/terraform-aws-modules/terraform-aws-s3-bucket/blob/master/main.tf
            ├── main.tf      
            ├── outputs.tf
            └── variables.tf
```



# Step 1: S3のRemote TF modulesを local Resource Modulesにコピー（Bottom up approach）

S3のRemote module: https://github.com/terraform-aws-modules/terraform-aws-s3-bucket

DynamoDBのTF doc: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/dynamodb_table

KMSのTF doc: https://registry.terraform.io/providers/hashicorp/aws/latest/docs/resources/kms_key



# Step 2: Terraform Remote BackendのInfrastructure Modulesを作成

[infrastructure_modules/terraform_remote_backend/main.tf](infrastructure_modules/terraform_remote_backend/main.tf)で、 S3 bucket, DynamoDB, KMS keyなどを定義します。


This `infrastructure_modules/terraform_remote_backend`はTerraform Remote Backendの __facade__ として、Sub-componentであるS3 bucket, DynamoDB, KMS keyなどをAbstractします。（__[Facade patternとは？](https://sourcemaking.com/design_patterns/facade)__）


![alt text](../imgs/facade_1.png "")
![alt text](../imgs/facade_2.png "")

> - Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use. 
> - Wrap a complicated subsystem with a simpler interface


```sh
# random integerをS3 bucketに付け加えて、Name collisionを防ぐ
resource "random_integer" "digits" {
  min = 1
  max = 100

  keepers = {
    # Generate a new integer each time s3_bucket_name value gets updated
    listener_arn = var.app_name
  }
}

module "s3_bucket_terraform_remote_backend" {  # <-------- STEP２
  source = "../../resource_modules/storage/s3"

  bucket        = local.bucket_name
  acl           = var.acl
  policy        = data.aws_iam_policy_document.bucket_policy.json
  tags          = local.tags
  force_destroy = var.force_destroy

  website                              = local.website
  cors_rule                            = local.cors_rule
  versioning                           = local.versioning
  logging                              = local.logging
  lifecycle_rule                       = local.lifecycle_rule
  replication_configuration            = local.replication_configuration
  server_side_encryption_configuration = local.server_side_encryption_configuration
  object_lock_configuration            = local.object_lock_configuration

  ## s3 bucket public access block ##
  block_public_policy     = var.block_public_policy
  block_public_acls       = var.block_public_acls
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}

########################################
## Dynamodb for TF state locking
########################################
module "dynamodb_terraform_state_lock" {  # <-------- STEP２
  source         = "../../resource_modules/database/dynamodb"
  name           = local.dynamodb_name
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity
  hash_key       = var.hash_key
  attribute_name = var.attribute_name
  attribute_type = var.attribute_type
  sse_enabled    = var.sse_enabled
  tags           = var.tags
}

########################################
## KMS
########################################
module "s3_kms_key_terraform_backend" {  # <-------- STEP２
  source = "../../resource_modules/identity/kms_key"

  name                    = local.ami_kms_key_name
  description             = local.ami_kms_key_description
  deletion_window_in_days = local.ami_kms_key_deletion_window_in_days
  tags                    = local.ami_kms_key_tags
  policy                  = data.aws_iam_policy_document.s3_terraform_states_kms_key_policy.json
  enable_key_rotation     = true
}
```



# Step 3: Composition layerを作成し、必要なインプット変数のValueを定義しInfra layerにパスダウン


[composition/terraform-remote-backend/ap-northeast-1/prod/main.tf](composition/terraform-remote-backend/ap-northeast-1/prod/main.tf)(main classのmain()が、他のクラスである`infrastructure_modules/terraform_remote_backend`のコンストラクターメソッドをコールしているのに似ている）

`composition/terraform-remote-backend/ap-northeast-1/prod/main.tf`は単に[infrastructure_modules/terraform_remote_backend/variables.tf](infrastructure_modules/terraform_remote_backend/variables.tf)で定義された必要なインプット変数をパスすればOK


```sh
########################################
# AWS Terraform backend composition
########################################
module "terraform_remote_backend" {  # <-------- STEP３
  source   = "../../../../infrastructure_modules/terraform_remote_backend"
  env      = var.env
  app_name = var.app_name
  region   = var.region
  tags     = local.tags

  ########################################
  ## Terraform State S3 Bucket
  ########################################
  acl                = var.acl
  force_destroy      = var.force_destroy
  versioning_enabled = var.versioning_enabled

  ## s3 bucket public access block ##
  block_public_policy     = var.block_public_policy
  block_public_acls       = var.block_public_acls
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets

  ########################################
  ## DynamoDB
  ########################################
  read_capacity  = var.read_capacity
  write_capacity = var.write_capacity
  hash_key       = var.hash_key
  attribute_name = var.attribute_name
  attribute_type = var.attribute_type
  sse_enabled    = var.sse_enabled
}
```



次にComposition layerのインプット変数を[composition/terraform-remote-backend/ap-northeast-1/prod/inputs.tf](composition/terraform-remote-backend/ap-northeast-1/prod/inputs.tf)定義します:

```sh
########################################
# Metadata
########################################
variable "env" {
  description = "The name of the environment."
  type = string
}

variable "app_name" {
  description = "The name of the application."
  type = string
}

variable "region" {
  description = "The AWS region this bucket should reside in."
  type = string
}

variable "tags" {
  description = "A mapping of tags to assign to the resources."
  type = map
}

########################################
## S3
########################################
variable "acl" {
  description = "The canned ACL to apply."
  type = string
}

variable "force_destroy" {
  description = "A boolean that indicates all objects should be deleted from the bucket so that the bucket can be destroyed without error. These objects are not recoverable."
  type = string
}

variable "versioning_enabled" {
  description = "Enable versioning. Once you version-enable a bucket, it can never return to an unversioned state."
  type = string
}

## s3 bucket public access block ##
variable "block_public_policy" {
  description = "Whether Amazon S3 should block public bucket policies for this bucket."
  type = string
}

variable "block_public_acls" {
  description = "Whether Amazon S3 should ignore public ACLs for this bucket."
  type = string
}

variable "ignore_public_acls" {
  description = "Whether Amazon S3 should ignore public ACLs for this bucket."
  type = string
}

variable "restrict_public_buckets" {
  description = "Whether Amazon S3 should restrict public bucket policies for this bucket."
  type = string
}

########################################
## DynamoDB
########################################
variable "read_capacity" {
  description = "The number of read units for this table."
  type = string
}

variable "write_capacity" {
  description = "The number of write units for this table."
  type = string
}

variable "hash_key" {
  description = "The attribute to use as the hash (partition) key."
  type = string
}

variable "attribute_name" {}

variable "attribute_type" {}

variable "sse_enabled" {
  description = "Encryption at rest using an AWS managed Customer Master Key. If enabled is false then server-side encryption is set to AWS owned CMK (shown as DEFAULT in the AWS console). If enabled is true then server-side encryption is set to AWS managed CMK (shown as KMS in the AWS console). ."
  type = string
}
```



最後にインプット変数のValueを[composition/terraform-remote-backend/ap-northeast-1/prod/terraform.tfvars](composition/terraform-remote-backend/ap-northeast-1/prod/terraform.tfvars)で指定します:

```sh
########################################
# Environment setting
########################################
region = "ap-northeast-1"
role_name    = "Admin"
profile_name = "aws-demo"
env = "prod"
application_name = "terraform-eks-demo-infra"
app_name = "terraform-eks-demo-infra"

########################################
## Terraform State S3 Bucket
########################################
acl = "private"
force_destroy = false
versioning_enabled = true

## s3 bucket public access block ##
block_public_policy = true
block_public_acls = true
ignore_public_acls = true
restrict_public_buckets = true

########################################
## DynamoDB
########################################
read_capacity = 5
write_capacity = 5
hash_key = "LockID"
sse_enabled = true # enable server side encryption
attribute_name = "LockID"
attribute_type = "S"
```



terraform apply
```sh
cd composition/terraform-remote-backend/ap-northeast-1/prod

# will use local backend because no S3 bucket is created yet to store tfstate file
terraform init

# usual stuff
terraform plan
terraform apply
```


```sh
$ terraform output

# Successful output
dynamodb_terraform_state_lock_arn = "arn:aws:dynamodb:ap-northeast-1:xxxxxx:table/dynamo-apne1-terraform-eks-demo-infra-prod-terraform-state-lock"
dynamodb_terraform_state_lock_id = "dynamo-apne1-terraform-eks-demo-infra-prod-terraform-state-lock"
s3_kms_terraform_backend_alias_arn = "arn:aws:kms:ap-northeast-1:xxxxxx:alias/cmk-apne1-prod-s3-terraform-backend"
s3_kms_terraform_backend_arn = "arn:aws:kms:ap-northeast-1:xxxxxx:key/4b6db186-df19-4402-adfd-fc0dfdc592bc"
s3_kms_terraform_backend_id = "4b6db186-df19-4402-adfd-fc0dfdc592bc"
s3_terraform_remote_backend_arn = "arn:aws:s3:::s3-apne1-terraform-eks-demo-infra-prod-terraform-backend-99"
s3_terraform_remote_backend_id = "s3-apne1-terraform-eks-demo-infra-prod-terraform-backend-99"
```

S3 bucketなどは作成されたので、このModuleの`terraform.tfstate`はマニュアルでS3にアップロードしてもOKです。