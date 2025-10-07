#!/bin/bash

# ECR Push Script for Data Streaming Pipeline
# This script builds and pushes Docker images to Amazon ECR

set -e

# Configuration
AWS_REGION=${AWS_REGION:-us-west-2}
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ECR_REGISTRY="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"

# Image configurations
declare -A IMAGES=(
    ["kafka-producer"]="kafka_producers"
    ["spark-jobs"]="spark_jobs"
    ["airflow"]="airflow"
    ["frontend"]="frontend"
)

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

# Login to ECR
ecr_login() {
    log_info "Logging in to Amazon ECR..."
    aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REGISTRY}
    log_info "Successfully logged in to ECR"
}

# Build and push a single image
build_and_push_image() {
    local image_name=$1
    local context_path=$2
    local tag=${3:-latest}
    
    log_info "Building image: ${image_name}"
    
    # Build the Docker image
    docker build -t ${image_name}:${tag} -f ${context_path}/Dockerfile ${context_path}
    
    # Tag for ECR
    local ecr_uri="${ECR_REGISTRY}/${image_name}:${tag}"
    docker tag ${image_name}:${tag} ${ecr_uri}
    
    # Push to ECR
    log_info "Pushing image to ECR: ${ecr_uri}"
    docker push ${ecr_uri}
    
    log_info "Successfully pushed ${image_name}:${tag}"
}

# Create ECR repositories if they don't exist
create_ecr_repositories() {
    log_info "Creating ECR repositories if they don't exist..."
    
    for image_name in "${!IMAGES[@]}"; do
        local repo_name="data-streaming-pipeline-${image_name}"
        
        # Check if repository exists
        if aws ecr describe-repositories --repository-names ${repo_name} --region ${AWS_REGION} &> /dev/null; then
            log_info "Repository ${repo_name} already exists"
        else
            log_info "Creating repository: ${repo_name}"
            aws ecr create-repository --repository-name ${repo_name} --region ${AWS_REGION}
            
            # Set lifecycle policy
            aws ecr put-lifecycle-policy --repository-name ${repo_name} --region ${AWS_REGION} --lifecycle-policy-text '{
                "rules": [
                    {
                        "rulePriority": 1,
                        "description": "Keep last 10 images",
                        "selection": {
                            "tagStatus": "tagged",
                            "countType": "imageCountMoreThan",
                            "countNumber": 10
                        },
                        "action": {
                            "type": "expire"
                        }
                    }
                ]
            }'
        fi
    done
}

# Main function
main() {
    local image_name=${1:-""}
    local tag=${2:-latest}
    
    log_info "Starting ECR push process..."
    log_info "AWS Region: ${AWS_REGION}"
    log_info "ECR Registry: ${ECR_REGISTRY}"
    
    # Check prerequisites
    check_aws_cli
    
    # Create ECR repositories
    create_ecr_repositories
    
    # Login to ECR
    ecr_login
    
    # Build and push images
    if [ -n "${image_name}" ]; then
        # Push specific image
        if [ -n "${IMAGES[$image_name]}" ]; then
            build_and_push_image "data-streaming-pipeline-${image_name}" "${IMAGES[$image_name]}" "${tag}"
        else
            log_error "Unknown image: ${image_name}"
            log_info "Available images: ${!IMAGES[@]}"
            exit 1
        fi
    else
        # Push all images
        for image_name in "${!IMAGES[@]}"; do
            build_and_push_image "data-streaming-pipeline-${image_name}" "${IMAGES[$image_name]}" "${tag}"
        done
    fi
    
    log_info "ECR push process completed successfully!"
}

# Show usage
show_usage() {
    echo "Usage: $0 [IMAGE_NAME] [TAG]"
    echo ""
    echo "Arguments:"
    echo "  IMAGE_NAME    Name of the image to build and push (optional)"
    echo "  TAG           Docker tag to use (default: latest)"
    echo ""
    echo "Available images:"
    for image_name in "${!IMAGES[@]}"; do
        echo "  - ${image_name}"
    done
    echo ""
    echo "Examples:"
    echo "  $0                    # Build and push all images"
    echo "  $0 kafka-producer     # Build and push only kafka-producer"
    echo "  $0 frontend v1.0.0    # Build and push frontend with tag v1.0.0"
}

# Handle command line arguments
case "${1:-}" in
    -h|--help)
        show_usage
        exit 0
        ;;
    *)
        main "$@"
        ;;
esac
