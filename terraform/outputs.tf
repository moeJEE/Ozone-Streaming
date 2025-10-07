# Data Streaming Pipeline - Outputs

output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = module.vpc.private_subnet_ids
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = module.vpc.public_subnet_ids
}

output "postgres_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.postgres.endpoint
  sensitive   = true
}

output "postgres_port" {
  description = "RDS instance port"
  value       = aws_db_instance.postgres.port
}

output "data_lake_bucket_name" {
  description = "Name of the data lake S3 bucket"
  value       = aws_s3_bucket.data_lake.bucket
}

output "backups_bucket_name" {
  description = "Name of the backups S3 bucket"
  value       = aws_s3_bucket.backups.bucket
}

output "ecr_repository_urls" {
  description = "URLs of the ECR repositories"
  value = {
    kafka_producer = aws_ecr_repository.kafka_producer.repository_url
    spark_jobs     = aws_ecr_repository.spark_jobs.repository_url
    airflow        = aws_ecr_repository.airflow.repository_url
    frontend       = aws_ecr_repository.frontend.repository_url
  }
}

output "cloudwatch_log_groups" {
  description = "CloudWatch log group names"
  value = {
    kafka  = aws_cloudwatch_log_group.kafka.name
    spark  = aws_cloudwatch_log_group.spark.name
    airflow = aws_cloudwatch_log_group.airflow.name
  }
}

output "security_group_ids" {
  description = "Security group IDs"
  value = {
    kafka    = aws_security_group.kafka.id
    postgres = aws_security_group.postgres.id
  }
}
