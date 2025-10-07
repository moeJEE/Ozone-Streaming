# Architecture Diagrams

This document contains visual representations of the Data Streaming Pipeline architecture.

## System Overview

```mermaid
graph TB
    subgraph "Data Sources"
        A[API Sources] --> B[Kafka Producers]
        C[JSON Files] --> B
        D[Database] --> B
    end
    
    subgraph "Streaming Layer"
        B --> E[Apache Kafka]
        E --> F[Topics]
    end
    
    subgraph "Processing Layer"
        F --> G[Spark Streaming]
        G --> H[Spark Batch]
        I[Airflow] --> G
        I --> H
    end
    
    subgraph "Storage Layer"
        H --> J[PostgreSQL]
        G --> J
    end
    
    subgraph "Visualization Layer"
        J --> K[Next.js Frontend]
        K --> L[Dashboard]
    end
    
    subgraph "Cloud Services"
        M[AWS S3] --> N[Backups]
        O[CloudWatch] --> P[Monitoring]
        Q[ECR] --> R[Docker Images]
    end
    
    J --> M
    G --> O
    H --> O
```

## Data Flow Diagram

```mermaid
sequenceDiagram
    participant DS as Data Sources
    participant KP as Kafka Producers
    participant K as Kafka
    participant SS as Spark Streaming
    participant SB as Spark Batch
    participant DB as PostgreSQL
    participant F as Frontend
    participant CW as CloudWatch
    
    DS->>KP: Raw Data
    KP->>K: Publish to Topics
    K->>SS: Stream Processing
    SS->>DB: Processed Data
    K->>SB: Batch Processing
    SB->>DB: Analytics Results
    DB->>F: Query Data
    F->>CW: Metrics
    SS->>CW: Metrics
    SB->>CW: Metrics
```

## Infrastructure Architecture

```mermaid
graph TB
    subgraph "AWS Cloud"
        subgraph "VPC"
            subgraph "Public Subnets"
                ALB[Application Load Balancer]
                NAT[NAT Gateway]
            end
            
            subgraph "Private Subnets"
                subgraph "ECS Cluster"
                    KAFKA[Kafka Container]
                    SPARK[Spark Container]
                    AIRFLOW[Airflow Container]
                    FRONTEND[Frontend Container]
                end
                
                subgraph "RDS"
                    POSTGRES[PostgreSQL]
                end
            end
        end
        
        subgraph "Storage"
            S3[S3 Buckets]
            ECR[ECR Repositories]
        end
        
        subgraph "Monitoring"
            CW[CloudWatch]
            SNS[SNS Alerts]
        end
    end
    
    subgraph "External"
        GITHUB[GitHub Actions]
        USERS[End Users]
    end
    
    GITHUB-->ECR
    ECR-->ECS
    USERS-->ALB
    ALB-->FRONTEND
    KAFKA-->POSTGRES
    SPARK-->POSTGRES
    AIRFLOW-->POSTGRES
    POSTGRES-->S3
    ECS-->CW
    CW-->SNS
```

## Component Interaction Diagram

```mermaid
graph LR
    subgraph "Data Ingestion"
        A1[API Producer] --> B1[Kafka Topic: raw_data]
        A2[JSON Producer] --> B1
        A3[Database Producer] --> B1
    end
    
    subgraph "Stream Processing"
        B1 --> C1[Spark Streaming]
        C1 --> C2[Data Transformation]
        C2 --> C3[Data Enrichment]
        C3 --> B2[Kafka Topic: processed_data]
    end
    
    subgraph "Batch Processing"
        B1 --> D1[Spark Batch]
        D1 --> D2[Data Aggregation]
        D2 --> D3[Analytics]
        D3 --> D4[PostgreSQL]
    end
    
    subgraph "Data Serving"
        B2 --> D4
        D4 --> E1[Next.js API]
        E1 --> E2[Frontend Dashboard]
    end
    
    subgraph "Orchestration"
        F1[Airflow DAG] --> C1
        F1 --> D1
        F1 --> G1[Backup Job]
        F1 --> G2[Monitoring Job]
    end
    
    subgraph "Monitoring"
        G2 --> H1[CloudWatch]
        C1 --> H1
        D1 --> H1
        D4 --> H1
    end
```

## Deployment Pipeline

```mermaid
graph TB
    subgraph "Development"
        A1[Code Commit] --> A2[Pre-commit Hooks]
        A2 --> A3[Unit Tests]
        A3 --> A4[Integration Tests]
    end
    
    subgraph "CI/CD"
        A4 --> B1[GitHub Actions]
        B1 --> B2[Build Docker Images]
        B2 --> B3[Push to ECR]
        B3 --> B4[Deploy to Staging]
        B4 --> B5[E2E Tests]
        B5 --> B6[Deploy to Production]
    end
    
    subgraph "Infrastructure"
        C1[Terraform Plan] --> C2[Terraform Apply]
        C2 --> C3[Create Resources]
        C3 --> C4[Configure Monitoring]
    end
    
    subgraph "Monitoring"
        D1[Health Checks] --> D2[Alerting]
        D2 --> D3[Incident Response]
    end
    
    B1 --> C1
    B6 --> D1
```

## Security Architecture

```mermaid
graph TB
    subgraph "Network Security"
        A1[VPC] --> A2[Security Groups]
        A2 --> A3[NACLs]
        A3 --> A4[Private Subnets]
    end
    
    subgraph "Application Security"
        B1[API Gateway] --> B2[Authentication]
        B2 --> B3[Authorization]
        B3 --> B4[Rate Limiting]
    end
    
    subgraph "Data Security"
        C1[Encryption at Rest] --> C2[S3 Encryption]
        C1 --> C3[RDS Encryption]
        C4[Encryption in Transit] --> C5[TLS/SSL]
        C4 --> C6[VPN]
    end
    
    subgraph "Monitoring Security"
        D1[CloudTrail] --> D2[Audit Logs]
        D2 --> D3[Security Alerts]
        D3 --> D4[Incident Response]
    end
```

## Scalability Architecture

```mermaid
graph TB
    subgraph "Horizontal Scaling"
        A1[Load Balancer] --> A2[Multiple Instances]
        A2 --> A3[Auto Scaling Groups]
        A3 --> A4[Health Checks]
    end
    
    subgraph "Data Scaling"
        B1[Kafka Partitions] --> B2[Consumer Groups]
        B2 --> B3[Spark Workers]
        B3 --> B4[Database Sharding]
    end
    
    subgraph "Storage Scaling"
        C1[S3] --> C2[Lifecycle Policies]
        C2 --> C3[Data Archival]
        C3 --> C4[Cost Optimization]
    end
    
    subgraph "Monitoring Scaling"
        D1[CloudWatch] --> D2[Custom Metrics]
        D2 --> D3[Auto Scaling Triggers]
        D3 --> D4[Resource Optimization]
    end
```

## Error Handling Flow

```mermaid
graph TB
    A[Error Occurs] --> B{Error Type}
    
    B -->|Network Error| C[Retry Logic]
    B -->|Data Error| D[Data Validation]
    B -->|System Error| E[System Recovery]
    
    C --> F[Exponential Backoff]
    F --> G[Max Retries Reached?]
    G -->|Yes| H[Dead Letter Queue]
    G -->|No| I[Retry]
    
    D --> J[Data Correction]
    J --> K[Continue Processing]
    
    E --> L[Health Check]
    L --> M[Service Restart]
    M --> N[Recovery Complete]
    
    H --> O[Manual Intervention]
    O --> P[Error Analysis]
    P --> Q[Fix Implementation]
```

## Backup and Recovery Flow

```mermaid
graph TB
    subgraph "Backup Process"
        A1[Scheduled Backup] --> A2[Database Snapshot]
        A2 --> A3[Data Export]
        A3 --> A4[S3 Upload]
        A4 --> A5[Verification]
    end
    
    subgraph "Recovery Process"
        B1[Recovery Request] --> B2[Backup Selection]
        B2 --> B3[Data Download]
        B3 --> B4[Database Restore]
        B4 --> B5[Data Validation]
        B5 --> B6[Service Restart]
    end
    
    subgraph "Monitoring"
        C1[Backup Status] --> C2[Success/Failure Alerts]
        C2 --> C3[Recovery Testing]
        C3 --> C4[RTO/RPO Metrics]
    end
```

## Performance Optimization

```mermaid
graph TB
    subgraph "Data Optimization"
        A1[Data Partitioning] --> A2[Index Optimization]
        A2 --> A3[Query Optimization]
        A3 --> A4[Caching Strategy]
    end
    
    subgraph "Processing Optimization"
        B1[Spark Tuning] --> B2[Memory Management]
        B2 --> B3[Parallel Processing]
        B3 --> B4[Resource Allocation]
    end
    
    subgraph "Network Optimization"
        C1[Connection Pooling] --> C2[Compression]
        C2 --> C3[CDN Usage]
        C3 --> C4[Load Balancing]
    end
    
    subgraph "Monitoring Optimization"
        D1[Performance Metrics] --> D2[Bottleneck Analysis]
        D2 --> D3[Optimization Recommendations]
        D3 --> D4[Continuous Improvement]
    end
```

## Cost Optimization

```mermaid
graph TB
    subgraph "Resource Optimization"
        A1[Right Sizing] --> A2[Auto Scaling]
        A2 --> A3[Spot Instances]
        A3 --> A4[Reserved Instances]
    end
    
    subgraph "Storage Optimization"
        B1[Lifecycle Policies] --> B2[Data Archival]
        B2 --> B3[Compression]
        B3 --> B4[Cleanup Jobs]
    end
    
    subgraph "Monitoring Costs"
        C1[Cost Alerts] --> C2[Budget Tracking]
        C2 --> C3[Cost Analysis]
        C3 --> C4[Optimization Actions]
    end
    
    subgraph "Automation"
        D1[Cost Automation] --> D2[Scheduled Scaling]
        D2 --> D3[Resource Cleanup]
        D3 --> D4[Cost Reporting]
    end
```

These diagrams provide a comprehensive visual representation of the Data Streaming Pipeline architecture, covering system overview, data flow, infrastructure, security, scalability, and operational aspects.
