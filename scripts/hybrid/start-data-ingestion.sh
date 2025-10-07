#!/bin/bash

# Start Data Ingestion Script for Hybrid Architecture
# This script starts all data ingestion processes

set -e

echo "🚀 Starting data ingestion processes..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Check if services are running
check_services() {
    log_info "Checking if services are running..."
    
    if ! docker-compose -f docker-compose.hybrid.yml ps | grep -q "Up"; then
        log_warn "Services are not running. Starting services..."
        docker-compose -f docker-compose.hybrid.yml up -d
        sleep 30
    fi
    
    log_info "Services are running"
}

# Start API producer
start_api_producer() {
    log_info "Starting API producer..."
    
    # Start in background
    nohup python3 data-sources/sample-api-producer.py > logs/api-producer.log 2>&1 &
    echo $! > logs/api-producer.pid
    
    log_info "API producer started (PID: $(cat logs/api-producer.pid))"
}

# Start JSON files producer
start_json_producer() {
    log_info "Starting JSON files producer..."
    
    # Start in background
    nohup python3 data-sources/sample-json-files.py > logs/json-producer.log 2>&1 &
    echo $! > logs/json-producer.pid
    
    log_info "JSON files producer started (PID: $(cat logs/json-producer.pid))"
}

# Start monitoring
start_monitoring() {
    log_info "Starting monitoring..."
    
    # Start CloudWatch metrics collection
    if [ -f "aws/cloudwatch-metrics.py" ]; then
        nohup python3 aws/cloudwatch-metrics.py > logs/cloudwatch-metrics.log 2>&1 &
        echo $! > logs/cloudwatch-metrics.pid
        log_info "CloudWatch metrics started (PID: $(cat logs/cloudwatch-metrics.pid))"
    fi
    
    # Start S3 backup
    if [ -f "aws/s3-backup-script.py" ]; then
        nohup python3 aws/s3-backup-script.py > logs/s3-backup.log 2>&1 &
        echo $! > logs/s3-backup.pid
        log_info "S3 backup started (PID: $(cat logs/s3-backup.pid))"
    fi
}

# Start frontend
start_frontend() {
    log_info "Starting frontend..."
    
    cd frontend
    nohup npm run dev > ../logs/frontend.log 2>&1 &
    echo $! > ../logs/frontend.pid
    cd ..
    
    log_info "Frontend started (PID: $(cat logs/frontend.pid))"
}

# Main function
main() {
    check_services
    start_api_producer
    start_json_producer
    start_monitoring
    start_frontend
    
    echo ""
    log_info "🎉 All data ingestion processes started!"
    echo ""
    echo "📊 Access your services:"
    echo "  Frontend Dashboard: http://localhost:3000"
    echo "  Airflow UI: http://localhost:8081"
    echo "  Spark Master: http://localhost:8080"
    echo ""
    echo "📝 Process logs:"
    echo "  API Producer: tail -f logs/api-producer.log"
    echo "  JSON Producer: tail -f logs/json-producer.log"
    echo "  Frontend: tail -f logs/frontend.log"
    echo "  CloudWatch: tail -f logs/cloudwatch-metrics.log"
    echo "  S3 Backup: tail -f logs/s3-backup.log"
    echo ""
    echo "🛑 To stop all processes: ./scripts/hybrid/stop-data-ingestion.sh"
}

# Run main function
main "$@"
