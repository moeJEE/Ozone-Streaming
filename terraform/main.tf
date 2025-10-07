# Data Streaming Pipeline - Main Terraform Configuration
terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  
  backend "s3" {
    bucket = "data-streaming-pipeline-terraform-state"
    key    = "terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
  
  default_tags {
    tags = {
      Project     = "data-streaming-pipeline"
      Environment = var.environment
      ManagedBy   = "terraform"
    }
  }
}

# Data sources
data "aws_availability_zones" "available" {
  state = "available"
}

data "aws_caller_identity" "current" {}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"
  
  name = "${var.project_name}-vpc"
  cidr = var.vpc_cidr
  
  azs             = slice(data.aws_availability_zones.available.names, 0, 2)
  private_subnets = var.private_subnet_cidrs
  public_subnets  = var.public_subnet_cidrs
  
  enable_nat_gateway = true
  enable_vpn_gateway = false
  enable_dns_hostnames = true
  enable_dns_support = true
  
  tags = {
    Name = "${var.project_name}-vpc"
  }
}

# Security Groups
resource "aws_security_group" "kafka" {
  name_prefix = "${var.project_name}-kafka-"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 9092
    to_port     = 9092
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  
  ingress {
    from_port   = 2181
    to_port     = 2181
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-kafka-sg"
  }
}

resource "aws_security_group" "postgres" {
  name_prefix = "${var.project_name}-postgres-"
  vpc_id      = module.vpc.vpc_id
  
  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = [var.vpc_cidr]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  tags = {
    Name = "${var.project_name}-postgres-sg"
  }
}

# S3 Buckets
resource "aws_s3_bucket" "data_lake" {
  bucket = "${var.project_name}-data-lake-${random_string.bucket_suffix.result}"
  
  tags = {
    Name        = "Data Lake"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "backups" {
  bucket = "${var.project_name}-backups-${random_string.bucket_suffix.result}"
  
  tags = {
    Name        = "Database Backups"
    Environment = var.environment
  }
}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "${var.project_name}-terraform-state-${random_string.bucket_suffix.result}"
  
  tags = {
    Name        = "Terraform State"
    Environment = var.environment
  }
}

# Random string for unique bucket names
resource "random_string" "bucket_suffix" {
  length  = 8
  special = false
  upper   = false
}

# S3 Bucket Versioning
resource "aws_s3_bucket_versioning" "data_lake" {
  bucket = aws_s3_bucket.data_lake.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "backups" {
  bucket = aws_s3_bucket.backups.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_versioning" "terraform_state" {
  bucket = aws_s3_bucket.terraform_state.id
  versioning_configuration {
    status = "Enabled"
  }
}

# ECR Repositories
resource "aws_ecr_repository" "kafka_producer" {
  name                 = "${var.project_name}-kafka-producer"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "spark_jobs" {
  name                 = "${var.project_name}-spark-jobs"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "airflow" {
  name                 = "${var.project_name}-airflow"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "frontend" {
  name                 = "${var.project_name}-frontend"
  image_tag_mutability = "MUTABLE"
  
  image_scanning_configuration {
    scan_on_push = true
  }
}

# RDS PostgreSQL
resource "aws_db_subnet_group" "postgres" {
  name       = "${var.project_name}-postgres-subnet-group"
  subnet_ids = module.vpc.private_subnets
  
  tags = {
    Name = "${var.project_name}-postgres-subnet-group"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-postgres"
  
  engine         = "postgres"
  engine_version = "15.4"
  instance_class = var.postgres_instance_class
  
  allocated_storage     = 20
  max_allocated_storage = 100
  storage_type          = "gp3"
  storage_encrypted     = true
  
  db_name  = var.postgres_db_name
  username = var.postgres_username
  password = var.postgres_password
  
  vpc_security_group_ids = [aws_security_group.postgres.id]
  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  
  backup_retention_period = 7
  backup_window          = "03:00-04:00"
  maintenance_window     = "sun:04:00-sun:05:00"
  
  skip_final_snapshot = var.environment == "development"
  deletion_protection = var.environment == "production"
  
  tags = {
    Name = "${var.project_name}-postgres"
  }
}

# CloudWatch Log Groups
resource "aws_cloudwatch_log_group" "kafka" {
  name              = "/aws/ecs/${var.project_name}/kafka"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "spark" {
  name              = "/aws/ecs/${var.project_name}/spark"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "airflow" {
  name              = "/aws/ecs/${var.project_name}/airflow"
  retention_in_days = 30
}

# CloudWatch Alarms
resource "aws_cloudwatch_metric_alarm" "postgres_cpu" {
  alarm_name          = "${var.project_name}-postgres-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors postgres cpu utilization"
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.postgres.id
  }
}

resource "aws_cloudwatch_metric_alarm" "postgres_connections" {
  alarm_name          = "${var.project_name}-postgres-connections"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "DatabaseConnections"
  namespace           = "AWS/RDS"
  period              = "300"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors postgres connections"
  
  dimensions = {
    DBInstanceIdentifier = aws_db_instance.postgres.id
  }
}
