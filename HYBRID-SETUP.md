# Hybrid Architecture Setup Guide

This guide will help you set up the hybrid data streaming pipeline with local processing and cloud backup/monitoring.

## 🏗️ **Architecture Overview**

### **Local Components (On Your Machine):**
- ✅ **Data Ingestion**: Kafka producers for APIs and JSON files
- ✅ **Stream Processing**: Apache Spark for real-time processing
- ✅ **Data Storage**: PostgreSQL for processed data
- ✅ **Orchestration**: Apache Airflow for workflow management
- ✅ **Frontend**: Next.js dashboard for visualization

### **Cloud Components (AWS):**
- ☁️ **S3 Backup**: Automated PostgreSQL backups
- ☁️ **CloudWatch**: Monitoring and alerting
- ☁️ **ECR**: Docker image storage (optional)

## 🚀 **Quick Start (3 Commands)**

```bash
# 1. Setup everything
make -f Makefile.hybrid setup

# 2. Start data ingestion
make -f Makefile.hybrid start

# 3. Check status
make -f Makefile.hybrid status
```

## 📋 **Detailed Setup Steps**

### **Step 1: Prerequisites**

**Required Software:**
- Docker & Docker Compose
- Python 3.9+
- Node.js 18+
- Git

**Optional (for cloud features):**
- AWS CLI
- AWS Account

### **Step 2: Clone and Setup**

```bash
# Clone repository
git clone <your-repo-url>
cd data-streaming-pipeline

# Setup hybrid architecture
make -f Makefile.hybrid setup
```

### **Step 3: Configure Environment**

```bash
# Edit configuration
nano config/.env

# Key settings to configure:
# - POSTGRES_PASSWORD: Set a secure password
# - AWS_ACCESS_KEY_ID: Your AWS access key (optional)
# - AWS_SECRET_ACCESS_KEY: Your AWS secret key (optional)
# - OPENWEATHER_API_KEY: For weather data (optional)
# - ALPHA_VANTAGE_API_KEY: For stock data (optional)
```

### **Step 4: Start Services**

```bash
# Start all services
make -f Makefile.hybrid start

# Check health
make -f Makefile.hybrid check-health
```

## 🌐 **Access Your Services**

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend Dashboard** | http://localhost:3000 | Real-time data visualization |
| **Airflow UI** | http://localhost:8081 | Workflow orchestration |
| **Spark Master** | http://localhost:8080 | Spark cluster management |
| **PostgreSQL** | localhost:5432 | Database (streaming_user/streaming_pass) |
| **Kafka** | localhost:9092 | Message broker |

## 📊 **Data Flow**

```
Data Sources → Kafka → Spark Streaming → PostgreSQL → Frontend Dashboard
     ↓
CloudWatch Monitoring + S3 Backups
```

## 🛠️ **Common Commands**

```bash
# View logs
make -f Makefile.hybrid logs

# Check status
make -f Makefile.hybrid status

# Stop everything
make -f Makefile.hybrid stop

# Restart
make -f Makefile.hybrid restart

# Run tests
make -f Makefile.hybrid test

# Manual backup
make -f Makefile.hybrid backup

# Clean everything
make -f Makefile.hybrid clean
```

## 🔧 **Configuration Options**

### **Local Processing Only (No Cloud)**
```bash
# Set in config/.env
ENABLE_CLOUDWATCH_MONITORING=false
ENABLE_S3_BACKUP=false
```

### **With Cloud Features**
```bash
# Set in config/.env
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
ENABLE_CLOUDWATCH_MONITORING=true
ENABLE_S3_BACKUP=true
```

## 📈 **Monitoring**

### **Local Monitoring**
- **Docker Logs**: `docker-compose -f docker-compose.hybrid.yml logs`
- **Application Logs**: `tail -f logs/*.log`
- **Health Checks**: `make -f Makefile.hybrid check-health`

### **Cloud Monitoring (if enabled)**
- **CloudWatch Dashboard**: AWS Console → CloudWatch
- **S3 Backups**: AWS Console → S3 → data-streaming-pipeline-backups
- **Logs**: AWS Console → CloudWatch → Log Groups

## 🚨 **Troubleshooting**

### **Services Not Starting**
```bash
# Check Docker
docker --version
docker-compose --version

# Check logs
make -f Makefile.hybrid logs

# Restart services
make -f Makefile.hybrid restart
```

### **Database Issues**
```bash
# Check PostgreSQL
docker-compose -f docker-compose.hybrid.yml exec postgres pg_isready -U streaming_user -d streaming_db

# Reset database
docker-compose -f docker-compose.hybrid.yml down -v
make -f Makefile.hybrid setup
```

### **Kafka Issues**
```bash
# Check Kafka topics
docker-compose -f docker-compose.hybrid.yml exec kafka kafka-topics --bootstrap-server localhost:9092 --list

# Check Kafka logs
docker-compose -f docker-compose.hybrid.yml logs kafka
```

### **Frontend Issues**
```bash
# Check frontend logs
tail -f logs/frontend.log

# Restart frontend
kill $(cat logs/frontend.pid) 2>/dev/null || true
cd frontend && npm run dev &
```

## 📝 **Data Sources**

### **Available Data Sources**
1. **API Producer**: Weather, stock, e-commerce data
2. **JSON Producer**: File-based data ingestion
3. **Database Producer**: Direct database connections

### **Start Data Sources**
```bash
# Start API producer
python3 data-sources/sample-api-producer.py

# Start JSON files producer
python3 data-sources/sample-json-files.py

# Or start all at once
make -f Makefile.hybrid start
```

## 🔄 **Backup and Recovery**

### **Automatic Backups (if cloud enabled)**
- **Frequency**: Every 6 hours
- **Location**: S3 bucket `data-streaming-pipeline-backups`
- **Retention**: 30 days

### **Manual Backup**
```bash
# Run manual backup
make -f Makefile.hybrid backup

# Check backup status
aws s3 ls s3://data-streaming-pipeline-backups/
```

## 🎯 **Next Steps**

1. **Customize Data Sources**: Modify `data-sources/` for your specific data
2. **Add Custom Processing**: Extend `spark_jobs/` for your business logic
3. **Configure Alerts**: Set up CloudWatch alarms for production
4. **Scale Up**: Add more Spark workers for higher throughput
5. **Security**: Implement proper authentication and authorization

## 🆘 **Support**

- **Documentation**: Check `docs/` directory
- **Issues**: Create a GitHub issue
- **Logs**: Always check logs first: `make -f Makefile.hybrid logs`

## 🎉 **Success Indicators**

You'll know everything is working when you see:
- ✅ All services showing "Healthy" in health check
- ✅ Data flowing in the frontend dashboard
- ✅ Kafka topics being created and populated
- ✅ PostgreSQL tables being populated
- ✅ CloudWatch metrics (if cloud enabled)
- ✅ S3 backups being created (if cloud enabled)

**Happy streaming! 🚀**
