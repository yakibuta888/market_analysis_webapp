# ------------------------------------------------
# Terraform Configuration File
# ------------------------------------------------
terraform {
  required_version = ">=1.9"
  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>5.0"
    }
  }
}

# ------------------------------------------------
# Provider Configuration
# ------------------------------------------------
provider "aws" {
  profile = "masanori"
  region = "ap-northeast-1"
}

# ------------------------------------------------
# Variables
# ------------------------------------------------
variable "project" {
  description = "Project Name"
  type = string
}

variable "environment" {
  description = "Environment Name"
  type = string
}

variable "vpc_cidr_block" {
  description = "VPC CIDR Block"
  type = string
}
