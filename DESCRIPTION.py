
# Save the Kafka-enhanced README content
 """# Data Engineering Pipeline with Kafka, Spark, Airflow, and Terraform

A production-ready, cloud-native data engineering pipeline featuring Apache Kafka for real-time streaming, Apache Spark for distributed processing, Apache Airflow for workflow orchestration, PostgreSQL for data serving, and Next.js for visualization. Infrastructure is fully automated using Terraform and CI/CD pipelines with GitHub Actions.

## 🏗️ Architecture Overview

The pipeline follows a modern, containerized architecture with clear separation of concerns across five primary layers, with AWS cloud services supporting the serving layer.

### Architecture Layers

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Visualization Layer                          │
│                            (Next.js)                                 │
└─────────────────────────────────────────────────────────────────────┘
                                  ↑
┌─────────────────────────────────────────────────────────────────────┐
│                          Serving Layer                               │
│                         (PostgreSQL)                                 │
│                               ↕                                      │
│                    ┌──────────────────────┐                         │
│                    │   AWS Cloud Layer    │                         │
│                    │  S3 | CloudWatch     │                         │
│                    └──────────────────────┘                         │
│                    ┌──────────────────────┐                         │
│                    │        CI/CD         │                         │
│                    │   GitHub Actions     │                         │
│                    └──────────────────────┘                         │
└─────────────────────────────────────────────────────────────────────┘
                                  ↑
┌─────────────────────────────────────────────────────────────────────┐
│                        Processing Layer                              │
│            Apache Spark Streaming (Master-Workers)                   │
│                    Orchestrated by Airflow                           │
└─────────────────────────────────────────────────────────────────────┘
                                  ↑
┌─────────────────────────────────────────────────────────────────────┐
│                      Streaming Layer                                 │
│              Apache Kafka (Broker)                                   │
└───────────────────────────────────────────────────────────────────── ┘
                                  ↑
┌─────────────────────────────────────────────────────────────────────┐
│                        Ingestion Layer                               │
│                      (JSON Data Sources)                             │
└─────────────────────────────────────────────────────────────────────┘
```

**Data Flow:** Ingestion → Kafka Streaming → Spark Processing → PostgreSQL Serving → Next.js Visualization

**Cloud Integration:** AWS S3 and CloudWatch are integrated with the serving layer for data backup/archival and monitoring.

All components are containerized using Docker and orchestrated through Apache Airflow for reliable, scheduled execution, with CI/CD automated via GitHub Actions for build, test, and deployment.

## 🚀 Tech Stack

### Core Technologies

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Orchestration** | Apache Airflow 3.0 | Workflow scheduling and DAG management |
| **Streaming** | Apache Kafka 4.1.0 | Real-time data streaming and message broker |
| **Processing** | Apache Spark 4.0.1 (Structured Streaming) | Distributed batch and stream processing |
| **Database** | PostgreSQL 15+ | Data serving and persistence |
| **Frontend** | Next.js 15 | Data visualization and dashboard |
| **Containerization** | Docker & Docker Compose | Application packaging and local development |

### Infrastructure & DevOps

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **IaC** | Terraform v1.13.3 | Infrastructure provisioning |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Cloud Storage** | AWS S3 | PostgreSQL backups and data archival |
| **Monitoring** | AWS CloudWatch | Database metrics, logs, and alerts |
| **Container Registry** | Amazon ECR | Docker image repository |

### Development Tools

- **Python compatible version** - Primary programming language
- **PySpark** - Spark Python API for batch and streaming
- **Kafka-Python** - Kafka client library
- **Pytest** - Unit and integration testing
- **Chispa** - DataFrame testing utilities
- **Pre-commit** - Code quality hooks

This architecture provides a complete streaming and batch processing solution with Apache Kafka enabling real-time data ingestion, Spark Structured Streaming for processing, PostgreSQL for serving, and comprehensive monitoring through AWS CloudWatch.
"""
