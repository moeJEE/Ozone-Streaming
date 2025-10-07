#!/bin/bash

# Hybrid Architecture Setup Script
# Local processing with cloud backup and monitoring

set -e

echo "🏗️ Setting up Hybrid Data Streaming Pipeline..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

# Check prerequisites
check_prerequisites() {
    log_step "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install Python 3.9 or higher."
        exit 1
    fi
    
    # Check AWS CLI (optional for cloud features)
    if ! command -v aws &> /dev/null; then
        log_warn "AWS CLI is not installed. Cloud features will be disabled."
        export ENABLE_CLOUD_FEATURES=false
    else
        if ! aws sts get-caller-identity &> /dev/null; then
            log_warn "AWS CLI is not configured. Cloud features will be disabled."
            export ENABLE_CLOUD_FEATURES=false
        else
            log_info "AWS CLI is configured and ready"
            export ENABLE_CLOUD_FEATURES=true
        fi
    fi
    
    log_info "Prerequisites check completed"
}

# Setup environment
setup_environment() {
    log_step "Setting up environment..."
    
    # Copy hybrid configuration
    if [ ! -f "config/.env" ]; then
        cp config/hybrid.env config/.env
        log_info "Created config/.env from hybrid template"
    else
        log_warn "config/.env already exists, skipping copy"
    fi
    
    # Create necessary directories
    mkdir -p data/raw
    mkdir -p data/processed
    mkdir -p logs
    mkdir -p monitoring/data
    
    log_info "Environment setup completed"
}

# Install Python dependencies
install_dependencies() {
    log_step "Installing Python dependencies..."
    
    # Install core dependencies
    pip3 install -r requirements.txt
    
    # Install AWS dependencies if cloud features are enabled
    if [ "$ENABLE_CLOUD_FEATURES" = true ]; then
        pip3 install -r aws/requirements.txt
        log_info "AWS dependencies installed"
    fi
    
    # Install data sources dependencies
    pip3 install -r data-sources/requirements.txt
    
    log_info "Dependencies installation completed"
}

# Setup local services
setup_local_services() {
    log_step "Setting up local services..."
    
    # Start local services
    docker-compose -f docker-compose.hybrid.yml up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to be ready..."
    sleep 30
    
    # Setup database
    log_info "Setting up database..."
    ./scripts/setup/setup_database.sh
    
    # Setup Kafka topics
    log_info "Setting up Kafka topics..."
    ./scripts/setup/setup_kafka.sh
    
    log_info "Local services setup completed"
}

# Setup cloud integration
setup_cloud_integration() {
    if [ "$ENABLE_CLOUD_FEATURES" = true ]; then
        log_step "Setting up cloud integration..."
        
        # Create S3 buckets
        log_info "Creating S3 buckets..."
        aws s3 mb s3://data-streaming-pipeline-backups --region us-west-2 || log_warn "Backup bucket may already exist"
        aws s3 mb s3://data-streaming-pipeline-data-lake --region us-west-2 || log_warn "Data lake bucket may already exist"
        
        # Setup CloudWatch monitoring
        log_info "Setting up CloudWatch monitoring..."
        ./monitoring/cloudwatch/setup-monitoring.sh --region us-west-2 --email alerts@company.com || log_warn "CloudWatch setup failed"
        
        log_info "Cloud integration setup completed"
    else
        log_warn "Skipping cloud integration setup (AWS not configured)"
    fi
}

# Setup monitoring
setup_monitoring() {
    log_step "Setting up monitoring..."
    
    # Create CloudWatch agent configuration
    cat > monitoring/cloudwatch/agent-config.json << EOF
{
    "logs": {
        "logs_collected": {
            "files": {
                "collect_list": [
                    {
                        "file_path": "/var/log/postgresql/postgresql.log",
                        "log_group_name": "/aws/local/data-streaming-pipeline/postgresql",
                        "log_stream_name": "{instance_id}"
                    },
                    {
                        "file_path": "/var/log/kafka/server.log",
                        "log_group_name": "/aws/local/data-streaming-pipeline/kafka",
                        "log_stream_name": "{instance_id}"
                    }
                ]
            }
        }
    },
    "metrics": {
        "namespace": "DataStreamingPipeline/Local",
        "metrics_collected": {
            "cpu": {
                "measurement": ["cpu_usage_idle", "cpu_usage_iowait"],
                "metrics_collection_interval": 60
            },
            "disk": {
                "measurement": ["used_percent"],
                "metrics_collection_interval": 60,
                "resources": ["*"]
            },
            "mem": {
                "measurement": ["mem_used_percent"],
                "metrics_collection_interval": 60
            }
        }
    }
}
EOF
    
    log_info "Monitoring setup completed"
}

# Setup data sources
setup_data_sources() {
    log_step "Setting up data sources..."
    
    # Generate sample data
    python3 data-sources/sample-json-files.py --generate-only
    
    log_info "Data sources setup completed"
}

# Run health checks
run_health_checks() {
    log_step "Running health checks..."
    
    # Check PostgreSQL
    if docker-compose -f docker-compose.hybrid.yml exec postgres pg_isready -U streaming_user -d streaming_db; then
        log_info "✅ PostgreSQL is healthy"
    else
        log_error "❌ PostgreSQL is not healthy"
        return 1
    fi
    
    # Check Kafka
    if docker-compose -f docker-compose.hybrid.yml exec kafka kafka-topics --bootstrap-server localhost:9092 --list > /dev/null 2>&1; then
        log_info "✅ Kafka is healthy"
    else
        log_error "❌ Kafka is not healthy"
        return 1
    fi
    
    # Check Spark Master
    if curl -f http://localhost:8080 > /dev/null 2>&1; then
        log_info "✅ Spark Master is healthy"
    else
        log_error "❌ Spark Master is not healthy"
        return 1
    fi
    
    # Check Airflow
    if curl -f http://localhost:8081/health > /dev/null 2>&1; then
        log_info "✅ Airflow is healthy"
    else
        log_error "❌ Airflow is not healthy"
        return 1
    fi
    
    log_info "All health checks passed!"
}

# Main function
main() {
    log_info "Starting Hybrid Data Streaming Pipeline setup..."
    
    check_prerequisites
    setup_environment
    install_dependencies
    setup_local_services
    setup_cloud_integration
    setup_monitoring
    setup_data_sources
    run_health_checks
    
    log_info "🎉 Hybrid setup completed successfully!"
    echo ""
    echo "📊 Access your services:"
    echo "  Frontend Dashboard: http://localhost:3000"
    echo "  Airflow UI: http://localhost:8081"
    echo "  Spark Master: http://localhost:8080"
    echo "  PostgreSQL: localhost:5432"
    echo "  Kafka: localhost:9092"
    echo ""
    echo "🚀 Next steps:"
    echo "  1. Start data ingestion: python3 data-sources/sample-api-producer.py"
    echo "  2. Start JSON files: python3 data-sources/sample-json-files.py"
    echo "  3. Start frontend: cd frontend && npm run dev"
    echo "  4. Setup monitoring: python3 aws/cloudwatch-metrics.py"
    echo ""
    if [ "$ENABLE_CLOUD_FEATURES" = true ]; then
        echo "☁️  Cloud features enabled:"
        echo "  - S3 backups: aws s3 ls s3://data-streaming-pipeline-backups"
        echo "  - CloudWatch: aws logs describe-log-groups"
    else
        echo "☁️  Cloud features disabled (configure AWS CLI to enable)"
    fi
}

# Run main function
main "$@"
