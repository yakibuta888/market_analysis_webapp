# ------------------------------------------------
# RDS parameter group
# ------------------------------------------------
resource "aws_db_parameter_group" "mysql_standalone_parametergroup" {
  name        = "${var.project}-${var.environment}-mysql-standalone-parametergroup"
  family      = "mysql8.0"
  description = "RDS parameter group"
  tags = {
    Name = "${var.project}-${var.environment}-mysql-standalone-parametergroup"
    Project = var.project
    Env = var.environment
  }

  parameter {
    name  = "character_set_database"
    value = "utf8mb4"
  }

  parameter {
    name  = "character_set_server"
    value = "utf8mb4"
  }
}

# ------------------------------------------------
# RDS option group
# ------------------------------------------------
resource "aws_db_option_group" "mysql_standalone_optiongroup" {
  name        = "${var.project}-${var.environment}-mysql-standalone-optiongroup"
  engine_name = "mysql"
  major_engine_version = "8.0"
  tags = {
    Name = "${var.project}-${var.environment}-mysql-standalone-optiongroup"
    Project = var.project
    Env = var.environment
  }
}

# ------------------------------------------------
# RDS subnet group
# ------------------------------------------------
resource "aws_db_subnet_group" "mysql_standalone_subnetgroup" {
  name        = "${var.project}-${var.environment}-mysql-standalone-subnetgroup"
  description = "RDS subnet group"
  subnet_ids  = aws_subnet.private.*.id

  tags = {
    Name = "${var.project}-${var.environment}-mysql-standalone-subnetgroup"
    Project = var.project
    Env = var.environment
  }
}

# ------------------------------------------------
# RDS instance
# ------------------------------------------------
resource "random_string" "db_password" {
  length  = 16
  special = false
}
