########################################
# AWS S3 Bucket resource module
#
# https://github.com/terraform-aws-modules/terraform-aws-s3-bucket
########################################
resource "aws_s3_bucket" "this" {
  count = var.create_bucket ? 1 : 0

  bucket              = var.bucket
  bucket_prefix       = var.bucket_prefix

  force_destroy       = var.force_destroy
  object_lock_enabled = var.object_lock_enabled
  tags                = var.tags

  dynamic "website" {
    for_each = length(keys(var.website)) == 0 ? [] : [var.website]

    content {
      index_document           = lookup(website.value, "index_document", null)
      error_document           = lookup(website.value, "error_document", null)
      redirect_all_requests_to = lookup(website.value, "redirect_all_requests_to", null)
      routing_rules            = lookup(website.value, "routing_rules", null)
    }
  }

  dynamic "cors_rule" {
    for_each = var.cors_rule

    content {
      allowed_methods = cors_rule.value.allowed_methods
      allowed_origins = cors_rule.value.allowed_origins
      allowed_headers = lookup(cors_rule.value, "allowed_headers", null)
      expose_headers  = lookup(cors_rule.value, "expose_headers", null)
      max_age_seconds = lookup(cors_rule.value, "max_age_seconds", null)
    }
  }

  dynamic "logging" {
    for_each = length(keys(var.logging)) == 0 ? [] : [var.logging]

    content {
      target_bucket = logging.value.target_bucket
      target_prefix = lookup(logging.value, "target_prefix", null)
    }
  }

  dynamic "grant" {
    for_each = var.grant

    content {
      id          = lookup(grant.value, "id", null)
      type        = grant.value.type
      permissions = grant.value.permissions
      uri         = lookup(grant.value, "uri", null)
    }
  }

  dynamic "lifecycle_rule" {
    for_each = var.lifecycle_rule

    content {
      id                                     = lookup(lifecycle_rule.value, "id", null)
      prefix                                 = lookup(lifecycle_rule.value, "prefix", null)
      tags                                   = lookup(lifecycle_rule.value, "tags", null)
      abort_incomplete_multipart_upload_days = lookup(lifecycle_rule.value, "abort_incomplete_multipart_upload_days", null)
      enabled                                = lifecycle_rule.value.enabled

      # Max 1 block - expiration
      dynamic "expiration" {
        for_each = length(keys(lookup(lifecycle_rule.value, "expiration", {}))) == 0 ? [] : [lookup(lifecycle_rule.value, "expiration", {})]

        content {
          date                         = lookup(expiration.value, "date", null)
          days                         = lookup(expiration.value, "days", null)
          expired_object_delete_marker = lookup(expiration.value, "expired_object_delete_marker", null)
        }
      }

      # Several blocks - transition
      dynamic "transition" {
        for_each = lookup(lifecycle_rule.value, "transition", [])

        content {
          date          = lookup(transition.value, "date", null)
          days          = lookup(transition.value, "days", null)
          storage_class = transition.value.storage_class
        }
      }

      # Max 1 block - noncurrent_version_expiration
      dynamic "noncurrent_version_expiration" {
        for_each = length(keys(lookup(lifecycle_rule.value, "noncurrent_version_expiration", {}))) == 0 ? [] : [lookup(lifecycle_rule.value, "noncurrent_version_expiration", {})]

        content {
          days = lookup(noncurrent_version_expiration.value, "days", null)
        }
      }

      # Several blocks - noncurrent_version_transition
      dynamic "noncurrent_version_transition" {
        for_each = lookup(lifecycle_rule.value, "noncurrent_version_transition", [])

        content {
          days          = lookup(noncurrent_version_transition.value, "days", null)
          storage_class = noncurrent_version_transition.value.storage_class
        }
      }
    }
  }

  # Max 1 block - replication_configuration
  dynamic "replication_configuration" {
    for_each = length(keys(var.replication_configuration)) == 0 ? [] : [var.replication_configuration]

    content {
      role = replication_configuration.value.role

      dynamic "rules" {
        for_each = replication_configuration.value.rules

        content {
          id       = lookup(rules.value, "id", null)
          priority = lookup(rules.value, "priority", null)
          prefix   = lookup(rules.value, "prefix", null)
          status   = rules.value.status

          dynamic "destination" {
            for_each = length(keys(lookup(rules.value, "destination", {}))) == 0 ? [] : [lookup(rules.value, "destination", {})]

            content {
              bucket             = destination.value.bucket
              storage_class      = lookup(destination.value, "storage_class", null)
              replica_kms_key_id = lookup(destination.value, "replica_kms_key_id", null)
              account_id         = lookup(destination.value, "account_id", null)

              dynamic "access_control_translation" {
                for_each = length(keys(lookup(destination.value, "access_control_translation", {}))) == 0 ? [] : [lookup(destination.value, "access_control_translation", {})]

                content {
                  owner = access_control_translation.value.owner
                }
              }
            }
          }

          dynamic "source_selection_criteria" {
            for_each = length(keys(lookup(rules.value, "source_selection_criteria", {}))) == 0 ? [] : [lookup(rules.value, "source_selection_criteria", {})]

            content {

              dynamic "sse_kms_encrypted_objects" {
                for_each = length(keys(lookup(source_selection_criteria.value, "sse_kms_encrypted_objects", {}))) == 0 ? [] : [lookup(source_selection_criteria.value, "sse_kms_encrypted_objects", {})]

                content {

                  enabled = sse_kms_encrypted_objects.value.enabled
                }
              }
            }
          }

          dynamic "filter" {
            for_each = length(keys(lookup(rules.value, "filter", {}))) == 0 ? [] : [lookup(rules.value, "filter", {})]

            content {
              prefix = lookup(filter.value, "prefix", null)
              tags   = lookup(filter.value, "tags", null)
            }
          }

        }
      }
    }
  }

  # Max 1 block - object_lock_configuration
  dynamic "object_lock_configuration" {
    for_each = length(keys(var.object_lock_configuration)) == 0 ? [] : [var.object_lock_configuration]

    content {

      dynamic "rule" {
        for_each = length(keys(lookup(object_lock_configuration.value, "rule", {}))) == 0 ? [] : [lookup(object_lock_configuration.value, "rule", {})]

        content {
          default_retention {
            mode  = lookup(lookup(rule.value, "default_retention", {}), "mode")
            days  = lookup(lookup(rule.value, "default_retention", {}), "days", null)
            years = lookup(lookup(rule.value, "default_retention", {}), "years", null)
          }
        }
      }
    }
  }

}

resource "aws_s3_bucket_versioning" "this" {
  count = var.create_bucket && length(keys(var.versioning)) > 0 ? 1 : 0
  bucket = aws_s3_bucket.this[0].id

  versioning_configuration {
    status    = lookup(var.versioning, "enabled", null) ? "Enabled" : "Suspended"
    mfa_delete = try(tobool(var.versioning["mfa_delete"]) ? "Enabled" : "Disabled", title(lower(var.versioning["mfa_delete"])), null)
  }
}

# Max 1 block - server_side_encryption_configuration
resource "aws_s3_bucket_server_side_encryption_configuration" "this" {
  count = var.create_bucket && length(keys(var.server_side_encryption_configuration)) > 0 ? 1 : 0

  bucket = aws_s3_bucket.this[0].id

  dynamic "rule" {
    for_each = try(flatten([var.server_side_encryption_configuration["rule"]]), [])

    content {
      bucket_key_enabled = try(rule.value.bucket_key_enabled, null)

      dynamic "apply_server_side_encryption_by_default" {
        for_each = length(keys(lookup(rule.value, "apply_server_side_encryption_by_default", {}))) == 0 ? [] : [
        lookup(rule.value, "apply_server_side_encryption_by_default", {})]

        content {
          sse_algorithm     = apply_server_side_encryption_by_default.value.sse_algorithm
          kms_master_key_id = lookup(apply_server_side_encryption_by_default.value, "kms_master_key_id", null)
        }
      }
    }
  }
}

# resource "aws_s3_bucket_acl" "this" {
#   count  = var.create_bucket && var.acl != null ? 1 : 0
#   bucket = aws_s3_bucket.this[0].id
#   acl    = var.acl

#   depends_on = [aws_s3_bucket_ownership_controls.this]
# }

resource "aws_s3_bucket_accelerate_configuration" "this" {
  count = var.create_bucket && var.acceleration_status != null ? 1 : 0

  bucket                = aws_s3_bucket.this[0].id

  # Valid values: "Enabled" or "Suspended"
  status = title(lower(var.acceleration_status))
}

resource "aws_s3_bucket_request_payment_configuration" "this" {
  count = var.create_bucket && var.request_payer != null ? 1 : 0

  bucket                = aws_s3_bucket.this[0].id

  # Valid values: "BucketOwner" or "Requester"
  payer = lower(var.request_payer) == "requester" ? "Requester" : "BucketOwner"
}

resource "aws_s3_bucket_policy" "this" {
  count = var.create_bucket && (var.attach_elb_log_delivery_policy || var.attach_policy) ? 1 : 0

  bucket = aws_s3_bucket.this[0].id
  policy = var.attach_elb_log_delivery_policy ? data.aws_iam_policy_document.elb_log_delivery[0].json : var.policy
}

# AWS Load Balancer access log delivery policy
data "aws_elb_service_account" "this" {
  count = var.create_bucket && var.attach_elb_log_delivery_policy ? 1 : 0
}

data "aws_iam_policy_document" "elb_log_delivery" {
  count = var.create_bucket && var.attach_elb_log_delivery_policy ? 1 : 0

  statement {
    sid = ""

    principals {
      type        = "AWS"
      identifiers = data.aws_elb_service_account.this.*.arn
    }

    effect = "Allow"

    actions = [
      "s3:PutObject",
    ]

    resources = [
      "${aws_s3_bucket.this[0].arn}/*",
    ]
  }
}

resource "aws_s3_bucket_public_access_block" "this" {
  count = var.create_bucket && var.attach_public_policy ? 1 : 0

  # Chain resources (s3_bucket -> s3_bucket_policy -> s3_bucket_public_access_block)
  # to prevent "A conflicting conditional operation is currently in progress against this resource."
  bucket = (var.attach_elb_log_delivery_policy || var.attach_policy) ? aws_s3_bucket_policy.this[0].id : aws_s3_bucket.this[0].id

  block_public_acls       = var.block_public_acls
  block_public_policy     = var.block_public_policy
  ignore_public_acls      = var.ignore_public_acls
  restrict_public_buckets = var.restrict_public_buckets
}

resource "aws_s3_bucket_ownership_controls" "this" {
  count = var.create_bucket && var.control_object_ownership ? 1 : 0

  bucket = var.attach_policy ? aws_s3_bucket_policy.this[0].id : aws_s3_bucket.this[0].id

  rule {
    object_ownership = var.object_ownership
  }

  # This `depends_on` is to prevent "A conflicting conditional operation is currently in progress against this resource."
  depends_on = [
    aws_s3_bucket_policy.this,
    aws_s3_bucket_public_access_block.this,
    aws_s3_bucket.this
  ]
}
