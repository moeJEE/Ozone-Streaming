# Data Streaming Pipeline - Variables

variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment name (development, staging, production)"
  type        = string
  default     = "development"
  
  validation {
    condition     = contains(["development", "staging", "production"], var.environment)
    error_message = "Environment must be one of: development, staging, production."
  }
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "data-streaming-pipeline"
}

variable "vpc_cidr" {
  description = "CIDR block for VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for private subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.101.0/24", "10.0.102.0/24"]
}

variable "postgres_instance_class" {
  description = "RDS instance class for PostgreSQL"
  type        = string
  default     = "db.t3.micro"
}

variable "postgres_db_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "streaming_db"
}

variable "postgres_username" {
  description = "Username for PostgreSQL"
  type        = string
  default     = "streaming_user"
}

variable "postgres_password" {
  description = "Password for PostgreSQL"
  type        = string
  sensitive   = true
}

variable "kafka_instance_type" {
  description = "EC2 instance type for Kafka"
  type        = string
  default     = "t3.medium"
}

variable "spark_instance_type" {
  description = "EC2 instance type for Spark"
  type        = string
  default     = "t3.large"
}

variable "airflow_instance_type" {
  description = "EC2 instance type for Airflow"
  type        = string
  default     = "t3.medium"
}

variable "frontend_instance_type" {
  description = "EC2 instance type for Frontend"
  type        = string
  default     = "t3.small"
}

variable "tags" {
  description = "Additional tags to apply to resources"
  type        = map(string)
  default     = {}
}
