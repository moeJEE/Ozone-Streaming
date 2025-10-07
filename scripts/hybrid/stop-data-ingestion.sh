#!/bin/bash

# Stop Data Ingestion Script for Hybrid Architecture
# This script stops all data ingestion processes

set -e

echo "🛑 Stopping data ingestion processes..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Stop process by PID file
stop_process() {
    local pid_file=$1
    local process_name=$2
    
    if [ -f "$pid_file" ]; then
        local pid=$(cat "$pid_file")
        if ps -p "$pid" > /dev/null 2>&1; then
            kill "$pid"
            log_info "Stopped $process_name (PID: $pid)"
        else
            log_warn "$process_name was not running"
        fi
        rm -f "$pid_file"
    else
        log_warn "PID file for $process_name not found"
    fi
}

# Stop all processes
stop_all_processes() {
    log_info "Stopping all data ingestion processes..."
    
    # Stop API producer
    stop_process "logs/api-producer.pid" "API Producer"
    
    # Stop JSON producer
    stop_process "logs/json-producer.pid" "JSON Producer"
    
    # Stop CloudWatch metrics
    stop_process "logs/cloudwatch-metrics.pid" "CloudWatch Metrics"
    
    # Stop S3 backup
    stop_process "logs/s3-backup.pid" "S3 Backup"
    
    # Stop frontend
    stop_process "logs/frontend.pid" "Frontend"
    
    log_info "All processes stopped"
}

# Stop Docker services
stop_docker_services() {
    log_info "Stopping Docker services..."
    
    docker-compose -f docker-compose.hybrid.yml down
    
    log_info "Docker services stopped"
}

# Cleanup
cleanup() {
    log_info "Cleaning up..."
    
    # Remove PID files
    rm -f logs/*.pid
    
    # Clean up any orphaned processes
    pkill -f "sample-api-producer.py" || true
    pkill -f "sample-json-files.py" || true
    pkill -f "cloudwatch-metrics.py" || true
    pkill -f "s3-backup-script.py" || true
    pkill -f "npm run dev" || true
    
    log_info "Cleanup completed"
}

# Main function
main() {
    stop_all_processes
    stop_docker_services
    cleanup
    
    log_info "🎉 All data ingestion processes stopped!"
    echo ""
    echo "📊 To restart:"
    echo "  ./scripts/hybrid/setup-hybrid.sh"
    echo "  ./scripts/hybrid/start-data-ingestion.sh"
}

# Run main function
main "$@"
