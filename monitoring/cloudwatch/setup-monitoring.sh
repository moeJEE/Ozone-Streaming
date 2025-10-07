#!/bin/bash

# CloudWatch Monitoring Setup Script
# This script sets up CloudWatch dashboards, alarms, and log groups

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-west-2}
NAMESPACE="DataStreamingPipeline"
SNS_TOPIC_ARN=${SNS_TOPIC_ARN:-""}

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
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

# Check if AWS CLI is installed and configured
check_aws_cli() {
    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI is not installed. Please install it first."
        exit 1
    fi
    
    if ! aws sts get-caller-identity &> /dev/null; then
        log_error "AWS CLI is not configured. Please run 'aws configure' first."
        exit 1
    fi
    
    log_info "AWS CLI is configured and ready"
}

# Create CloudWatch log groups
create_log_groups() {
    log_info "Creating CloudWatch log groups..."
    
    local log_groups=(
        "/aws/ecs/data-streaming-pipeline/kafka"
        "/aws/ecs/data-streaming-pipeline/spark"
        "/aws/ecs/data-streaming-pipeline/airflow"
        "/aws/ecs/data-streaming-pipeline/frontend"
    )
    
    for log_group in "${log_groups[@]}"; do
        if aws logs describe-log-groups --log-group-name-prefix "$log_group" --region $AWS_REGION | grep -q "$log_group"; then
            log_info "Log group $log_group already exists"
        else
            aws logs create-log-group --log-group-name "$log_group" --region $AWS_REGION
            aws logs put-retention-policy --log-group-name "$log_group" --retention-in-days 30 --region $AWS_REGION
            log_info "Created log group: $log_group"
        fi
    done
}

# Create CloudWatch dashboard
create_dashboard() {
    log_info "Creating CloudWatch dashboard..."
    
    local dashboard_name="DataStreamingPipeline-Dashboard"
    local dashboard_body=$(cat monitoring/cloudwatch/dashboards/data-pipeline-dashboard.json)
    
    aws cloudwatch put-dashboard \
        --dashboard-name "$dashboard_name" \
        --dashboard-body "$dashboard_body" \
        --region $AWS_REGION
    
    log_info "Created dashboard: $dashboard_name"
}

# Create SNS topic for alerts
create_sns_topic() {
    if [ -z "$SNS_TOPIC_ARN" ]; then
        log_info "Creating SNS topic for alerts..."
        
        local topic_name="data-pipeline-alerts"
        local topic_arn=$(aws sns create-topic --name "$topic_name" --region $AWS_REGION --query 'TopicArn' --output text)
        
        # Subscribe email (you'll need to confirm the subscription)
        if [ -n "$ALERT_EMAIL" ]; then
            aws sns subscribe \
                --topic-arn "$topic_arn" \
                --protocol email \
                --notification-endpoint "$ALERT_EMAIL" \
                --region $AWS_REGION
            log_info "Subscribed $ALERT_EMAIL to topic $topic_name"
        fi
        
        SNS_TOPIC_ARN="$topic_arn"
        log_info "Created SNS topic: $topic_arn"
    else
        log_info "Using existing SNS topic: $SNS_TOPIC_ARN"
    fi
}

# Create CloudWatch alarms
create_alarms() {
    log_info "Creating CloudWatch alarms..."
    
    local alarms_file="monitoring/cloudwatch/alarms/alarms.json"
    
    if [ ! -f "$alarms_file" ]; then
        log_error "Alarms file not found: $alarms_file"
        return 1
    fi
    
    # Update SNS topic ARN in alarms
    local temp_alarms_file=$(mktemp)
    sed "s/123456789012/$(aws sts get-caller-identity --query Account --output text)/g" "$alarms_file" > "$temp_alarms_file"
    sed "s/us-west-2/$AWS_REGION/g" "$temp_alarms_file" > "$temp_alarms_file.tmp" && mv "$temp_alarms_file.tmp" "$temp_alarms_file"
    
    # Create alarms
    jq -r '.alarms[] | @base64' "$temp_alarms_file" | while read -r alarm; do
        alarm_json=$(echo "$alarm" | base64 --decode)
        alarm_name=$(echo "$alarm_json" | jq -r '.AlarmName')
        
        if aws cloudwatch describe-alarms --alarm-names "$alarm_name" --region $AWS_REGION | grep -q "$alarm_name"; then
            log_info "Alarm $alarm_name already exists"
        else
            aws cloudwatch put-metric-alarm --cli-input-json "$alarm_json" --region $AWS_REGION
            log_info "Created alarm: $alarm_name"
        fi
    done
    
    rm -f "$temp_alarms_file"
}

# Create custom metrics
create_custom_metrics() {
    log_info "Setting up custom metrics..."
    
    # This would typically be done by your application
    # For now, we'll just log the metrics that should be sent
    log_info "Custom metrics to be sent by your application:"
    echo "  - database_connections"
    echo "  - total_records"
    echo "  - processed_records"
    echo "  - processing_rate"
    echo "  - kafka_messages_per_second"
    echo "  - kafka_consumer_lag"
    echo "  - spark_jobs_running"
    echo "  - error_rate"
}

# Main function
main() {
    log_info "Setting up CloudWatch monitoring for Data Streaming Pipeline..."
    log_info "AWS Region: $AWS_REGION"
    
    # Check prerequisites
    check_aws_cli
    
    # Create resources
    create_log_groups
    create_dashboard
    create_sns_topic
    create_alarms
    create_custom_metrics
    
    log_info "CloudWatch monitoring setup completed successfully!"
    log_info ""
    log_info "Next steps:"
    log_info "1. Confirm SNS email subscription if you provided an email"
    log_info "2. Start sending custom metrics from your application"
    log_info "3. View the dashboard in CloudWatch console"
    log_info "4. Set up additional alerts as needed"
}

# Show usage
show_usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  -r, --region REGION     AWS region (default: us-west-2)"
    echo "  -e, --email EMAIL       Email for SNS alerts"
    echo "  -t, --topic-arn ARN     Existing SNS topic ARN"
    echo "  -h, --help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 --region us-east-1 --email alerts@company.com"
    echo "  $0 --topic-arn arn:aws:sns:us-west-2:123456789012:alerts"
}

# Handle command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -r|--region)
            AWS_REGION="$2"
            shift 2
            ;;
        -e|--email)
            ALERT_EMAIL="$2"
            shift 2
            ;;
        -t|--topic-arn)
            SNS_TOPIC_ARN="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        *)
            log_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Run main function
main
