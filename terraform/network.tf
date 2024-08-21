# ------------------------------------------------
# VPC
# ------------------------------------------------
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr_block
  instance_tenancy = "default"
  enable_dns_support = true
  enable_dns_hostnames = true
  assign_generated_ipv6_cidr_block = false

  tags = {
    Name = "${var.project}-${var.environment}-vpc"
    Project = var.project
    Env = var.environment
  }
}

# ------------------------------------------------
# Subnet
# ------------------------------------------------
resource "aws_subnet" "public" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index+1)
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = true

  tags = {
    Name = "${var.project}-${var.environment}-public-subnet-${count.index}"
    Project = var.project
    Env = var.environment
    Type = "public"
  }
}

resource "aws_subnet" "private" {
  count = 2
  vpc_id = aws_vpc.main.id
  cidr_block = cidrsubnet(aws_vpc.main.cidr_block, 4, count.index+3)
  availability_zone = element(data.aws_availability_zones.available.names, count.index)
  map_public_ip_on_launch = false

  tags = {
    Name = "${var.project}-${var.environment}-private-subnet-${count.index}"
    Project = var.project
    Env = var.environment
    Type = "private"
  }
}

data "aws_availability_zones" "available" {
  state = "available"
}

# ------------------------------------------------
# Route Table
# ------------------------------------------------
resource "aws_route_table" "public_rt" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-public-rt"
    Project = var.project
    Env = var.environment
    Type = "public"
  }
}

resource "aws_route_table_association" "public_rt_association" {
  count = 2
  subnet_id = element(aws_subnet.public[*].id, count.index)
  route_table_id = aws_route_table.public_rt.id
}

resource "aws_route_table" "private_rt" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-private-rt"
    Project = var.project
    Env = var.environment
    Type = "private"
  }
}

resource "aws_route_table_association" "private_rt_association" {
  count = 2
  subnet_id = element(aws_subnet.private[*].id, count.index)
  route_table_id = aws_route_table.private_rt.id
}

# ------------------------------------------------
# Internet Gateway
# ------------------------------------------------
resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "${var.project}-${var.environment}-igw"
    Project = var.project
    Env = var.environment
  }
}

resource "aws_route" "public_rt_igw_route" {
  route_table_id = aws_route_table.public_rt.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id = aws_internet_gateway.igw.id
}
