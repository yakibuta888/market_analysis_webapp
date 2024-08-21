# ------------------------------------------------
# Security Group
# ------------------------------------------------
# frontend security group
resource "aws_security_group" "frontend_sg" {
  name        = "${var.project}-${var.environment}-frontend-sg"
  description = "frontend security group"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-frontend-sg"
    Project = var.project
    Env = var.environment
  }
}

resource "aws_security_group_rule" "frontend_in_http" {
  security_group_id = aws_security_group.frontend_sg.id
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "frontend_in_https" {
  security_group_id = aws_security_group.frontend_sg.id
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "frontend_out_tcp8000" {
  security_group_id = aws_security_group.frontend_sg.id
  type              = "egress"
  protocol          = "tcp"
  from_port         = 8000
  to_port           = 8000
  source_security_group_id = aws_security_group.backend_sg.id
}

# backend security group
resource "aws_security_group" "backend_sg" {
  name        = "${var.project}-${var.environment}-backend-sg"
  description = "backend security group"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-backend-sg"
    Project = var.project
    Env = var.environment
  }
}

resource "aws_security_group_rule" "backend_in_tcp8000" {
  security_group_id = aws_security_group.backend_sg.id
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 8000
  to_port           = 8000
  source_security_group_id = aws_security_group.frontend_sg.id
}

resource "aws_security_group_rule" "backend_out_tcp3306" {
  security_group_id = aws_security_group.backend_sg.id
  type              = "egress"
  protocol          = "tcp"
  from_port         = 3306
  to_port           = 3306
  source_security_group_id = aws_security_group.db_sg.id
}

# opmng security group
resource "aws_security_group" "opmng_sg" {
  name        = "${var.project}-${var.environment}-opmng-sg"
  description = "operation and managemant security group"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-opmng-sg"
    Project = var.project
    Env = var.environment
  }
}

resource "aws_security_group_rule" "opmng_in_ssh" {
  security_group_id = aws_security_group.opmng_sg.id
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 22
  to_port           = 22
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "opmng_in_tcp8000" {
  security_group_id = aws_security_group.opmng_sg.id
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 8000
  to_port           = 8000
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "opmng_out_http" {
  security_group_id = aws_security_group.opmng_sg.id
  type              = "egress"
  protocol          = "tcp"
  from_port         = 80
  to_port           = 80
  cidr_blocks       = ["0.0.0.0/0"]
}

resource "aws_security_group_rule" "opmng_out_https" {
  security_group_id = aws_security_group.opmng_sg.id
  type              = "egress"
  protocol          = "tcp"
  from_port         = 443
  to_port           = 443
  cidr_blocks       = ["0.0.0.0/0"]
}

# db security group
resource "aws_security_group" "db_sg" {
  name        = "${var.project}-${var.environment}-db-sg"
  description = "database security group"
  vpc_id      = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-db-sg"
    Project = var.project
    Env = var.environment
  }
}

resource "aws_security_group_rule" "db_in_tcp3306" {
  security_group_id = aws_security_group.db_sg.id
  type              = "ingress"
  protocol          = "tcp"
  from_port         = 3306
  to_port           = 3306
  source_security_group_id = aws_security_group.backend_sg.id
}
