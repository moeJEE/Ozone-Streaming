# Deployment Guide

This guide provides comprehensive instructions for deploying the Data Streaming Pipeline across different environments.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Local Development](#local-development)
- [Staging Deployment](#staging-deployment)
- [Production Deployment](#production-deployment)
- [AWS Cloud Deployment](#aws-cloud-deployment)
- [Monitoring Setup](#monitoring-setup)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### System Requirements

- **Operating System**: Linux, macOS, or Windows with WSL2
- **Memory**: Minimum 8GB RAM (16GB recommended for production)
- **Storage**: Minimum 20GB free space
- **CPU**: 4 cores minimum (8 cores recommended for production)

### Software Requirements

- **Docker**: Version 20.10 or higher
- **Docker Compose**: Version 2.0 or higher
- **Python**: Version 3.9 or higher
- **Node.js**: Version 18 or higher (for frontend)
- **Terraform**: Version 1.0 or higher (for infrastructure)
- **AWS CLI**: Version 2.0 or higher (for cloud deployment)

### AWS Requirements (for cloud deployment)

- AWS Account with appropriate permissions
- IAM user with programmatic access
- S3 bucket for Terraform state
- ECR repositories for Docker images

## Environment Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd data-streaming-pipeline
```

### 2. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install
cd ..

# Install pre-commit hooks
pre-commit install
```

### 3. Environment Configuration

```bash
# Copy environment template
cp config/.env.example config/.env

# Edit configuration
nano config/.env
```

**Required Environment Variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql://streaming_user:streaming_pass@localhost:5432/streaming_db
POSTGRES_DB=streaming_db
POSTGRES_USER=streaming_user
POSTGRES_PASSWORD=your_secure_password

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC_RAW_DATA=raw_data
KAFKA_TOPIC_PROCESSED_DATA=processed_data

# Spark Configuration
SPARK_MASTER=spark://localhost:7077
SPARK_APP_NAME=streaming_pipeline

# AWS Configuration (for cloud deployment)
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_DEFAULT_REGION=us-west-2

# API Keys (optional)
OPENWEATHER_API_KEY=your_openweather_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
```

## Local Development

### 1. Start Services

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 2. Initialize Database

```bash
# Run database setup
./scripts/setup/setup_database.sh

# Run migrations
./scripts/setup/run_migrations.sh
```

### 3. Setup Kafka Topics

```bash
# Create Kafka topics
./scripts/setup/setup_kafka.sh
```

### 4. Start Data Ingestion

```bash
# Start API producer
python data-sources/sample-api-producer.py

# Start JSON files producer
python data-sources/sample-json-files.py
```

### 5. Start Frontend

```bash
cd frontend
npm run dev
```

### 6. Access Services

- **Frontend Dashboard**: http://localhost:3000
- **Airflow UI**: http://localhost:8081
- **Spark Master**: http://localhost:8080
- **Kafka**: localhost:9092

## Staging Deployment

### 1. Prepare Staging Environment

```bash
# Set environment
export ENVIRONMENT=staging

# Update configuration
cp config/staging.env config/.env
```

### 2. Deploy Infrastructure

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan deployment
terraform plan -var="environment=staging"

# Apply changes
terraform apply -var="environment=staging"
```

### 3. Deploy Applications

```bash
# Build and push Docker images
./aws/ecr-push.sh

# Deploy to ECS/Fargate
aws ecs update-service --cluster staging-cluster --service data-pipeline-service --force-new-deployment
```

### 4. Setup Monitoring

```bash
# Setup CloudWatch monitoring
./monitoring/cloudwatch/setup-monitoring.sh --region us-west-2 --email alerts@company.com
```

## Production Deployment

### 1. Prepare Production Environment

```bash
# Set environment
export ENVIRONMENT=production

# Update configuration
cp config/prod.env config/.env
```

### 2. Security Hardening

```bash
# Generate secure passwords
openssl rand -base64 32

# Update SSL certificates
# Configure firewall rules
# Setup VPN access
```

### 3. Deploy Infrastructure

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan deployment
terraform plan -var="environment=production"

# Apply changes (requires confirmation)
terraform apply -var="environment=production"
```

### 4. Deploy Applications

```bash
# Build and push Docker images
./aws/ecr-push.sh

# Deploy to ECS/Fargate
aws ecs update-service --cluster production-cluster --service data-pipeline-service --force-new-deployment
```

### 5. Setup Monitoring and Alerts

```bash
# Setup CloudWatch monitoring
./monitoring/cloudwatch/setup-monitoring.sh --region us-west-2 --email production-alerts@company.com

# Setup log aggregation
# Configure alerting rules
# Setup backup procedures
```

## AWS Cloud Deployment

### 1. Prerequisites

```bash
# Configure AWS CLI
aws configure

# Create S3 bucket for Terraform state
aws s3 mb s3://data-streaming-pipeline-terraform-state

# Create ECR repositories
aws ecr create-repository --repository-name data-streaming-pipeline-kafka-producer
aws ecr create-repository --repository-name data-streaming-pipeline-spark-jobs
aws ecr create-repository --repository-name data-streaming-pipeline-airflow
aws ecr create-repository --repository-name data-streaming-pipeline-frontend
```

### 2. Deploy Infrastructure

```bash
# Initialize Terraform
cd terraform
terraform init

# Plan deployment
terraform plan

# Apply changes
terraform apply
```

### 3. Deploy Applications

```bash
# Build and push Docker images
./aws/ecr-push.sh

# Deploy to ECS
aws ecs create-cluster --cluster-name data-streaming-pipeline-cluster
aws ecs create-service --cluster data-streaming-pipeline-cluster --service-name data-pipeline-service --task-definition data-pipeline-task
```

### 4. Setup CI/CD

```bash
# Configure GitHub Actions secrets
# AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY
# POSTGRES_PASSWORD
# AWS_ACCOUNT_ID
```

## Monitoring Setup

### 1. CloudWatch Setup

```bash
# Setup CloudWatch monitoring
./monitoring/cloudwatch/setup-monitoring.sh --region us-west-2 --email alerts@company.com
```

### 2. Custom Metrics

```bash
# Start metrics collection
python aws/cloudwatch-metrics.py
```

### 3. Log Aggregation

```bash
# Setup log groups
aws logs create-log-group --log-group-name /aws/ecs/data-streaming-pipeline

# Configure log streams
aws logs create-log-stream --log-group-name /aws/ecs/data-streaming-pipeline --log-stream-name kafka
```

### 4. Alerting

```bash
# Create SNS topic
aws sns create-topic --name data-pipeline-alerts

# Subscribe to alerts
aws sns subscribe --topic-arn arn:aws:sns:us-west-2:123456789012:data-pipeline-alerts --protocol email --notification-endpoint alerts@company.com
```

## Troubleshooting

### Common Issues

#### 1. Docker Compose Issues

```bash
# Check logs
docker-compose logs -f

# Restart services
docker-compose restart

# Clean up
docker-compose down -v
docker system prune -f
```

#### 2. Database Connection Issues

```bash
# Check database status
docker-compose exec postgres pg_isready -U streaming_user -d streaming_db

# Check logs
docker-compose logs postgres
```

#### 3. Kafka Issues

```bash
# Check Kafka status
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Check logs
docker-compose logs kafka
```

#### 4. Spark Issues

```bash
# Check Spark status
curl http://localhost:8080

# Check logs
docker-compose logs spark-master
```

#### 5. Airflow Issues

```bash
# Check Airflow status
curl http://localhost:8081/health

# Check logs
docker-compose logs airflow-webserver
```

### Performance Optimization

#### 1. Database Optimization

```sql
-- Create indexes
CREATE INDEX idx_raw_data_created_at ON raw_data(created_at);
CREATE INDEX idx_raw_data_source ON raw_data(source);

-- Analyze tables
ANALYZE raw_data;
ANALYZE processed_data;
```

#### 2. Kafka Optimization

```bash
# Increase partition count
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --alter --topic raw_data --partitions 6

# Increase replication factor
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --alter --topic raw_data --partitions 6 --replication-factor 3
```

#### 3. Spark Optimization

```python
# Configure Spark for better performance
spark.conf.set("spark.sql.adaptive.enabled", "true")
spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")
spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
```

### Backup and Recovery

#### 1. Database Backup

```bash
# Create backup
./aws/s3-backup-script.py

# Restore backup
docker-compose exec postgres psql -U streaming_user -d streaming_db -f /backup/restore.sql
```

#### 2. Configuration Backup

```bash
# Backup configuration
tar -czf config-backup-$(date +%Y%m%d).tar.gz config/

# Restore configuration
tar -xzf config-backup-20240101.tar.gz
```

### Security Considerations

#### 1. Network Security

```bash
# Configure firewall rules
ufw allow 5432/tcp  # PostgreSQL
ufw allow 9092/tcp  # Kafka
ufw allow 8080/tcp  # Spark
ufw allow 8081/tcp  # Airflow
```

#### 2. Data Encryption

```bash
# Enable SSL for PostgreSQL
# Enable SASL for Kafka
# Use HTTPS for frontend
```

#### 3. Access Control

```bash
# Setup IAM roles
# Configure RBAC
# Enable MFA
```

## Maintenance

### Regular Tasks

#### Daily
- Check service health
- Monitor resource usage
- Review error logs

#### Weekly
- Update dependencies
- Clean up old data
- Review performance metrics

#### Monthly
- Security updates
- Backup verification
- Capacity planning

### Updates and Upgrades

#### 1. Application Updates

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt
npm install

# Restart services
docker-compose restart
```

#### 2. Infrastructure Updates

```bash
# Update Terraform
cd terraform
terraform plan
terraform apply
```

#### 3. Database Migrations

```bash
# Run migrations
./scripts/setup/run_migrations.sh
```

## Support

For additional support:

- **Documentation**: Check the docs/ directory
- **Issues**: Create a GitHub issue
- **Discussions**: Use GitHub discussions
- **Email**: Contact the development team

## Conclusion

This deployment guide provides comprehensive instructions for deploying the Data Streaming Pipeline across different environments. Follow the steps carefully and refer to the troubleshooting section if you encounter any issues.
