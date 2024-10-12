########################################
# Provider to connect to AWS
#
# https://www.terraform.io/docs/providers/aws/
########################################

terraform {
  required_version = ">= 1.9"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # use local backend to first create S3 bucket to store .tfstate later
  backend "s3" {
    bucket = "s3-apne1-market-analysis-webapp-prod-terraform-backend-93"
    key = "infra/ap-northeast-1/prod/terraform.tfstate"
    region = "ap-northeast-1"
    profile = "masanori"
    dynamodb_table = "dynamo-apne1-market-analysis-webapp-prod-terraform-state-lock"
    encrypt = true
  }
}

########################################
# Provider Configuration
########################################
provider "aws" {
  region = var.region
  profile = var.profile_name
}
