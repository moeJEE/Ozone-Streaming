# Data Streaming Pipeline

A comprehensive data streaming pipeline built with Apache Kafka, Apache Spark, Apache Airflow, and PostgreSQL.

## 🏗️ Architecture

This pipeline processes real-time data through the following components:

- **Data Ingestion**: Kafka producers collect data from various sources
- **Stream Processing**: Apache Spark processes data in real-time
- **Batch Processing**: Apache Spark handles historical data and complex analytics
- **Orchestration**: Apache Airflow manages workflows and scheduling
- **Storage**: PostgreSQL for structured data storage
- **Monitoring**: Prometheus and Grafana for observability

## 🚀 Quick Start

1. **Clone and setup**
   ```bash
   git clone <repository-url>
   cd data-streaming-pipeline
   chmod +x scripts/setup/*.sh scripts/deploy/*.sh scripts/monitoring/*.sh
   ```

2. **Configure environment**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your settings
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

4. **Run tests**
   ```bash
   make test
   ```

## 📁 Project Structure

```
data-streaming-pipeline/
├── .github/workflows/          # CI/CD pipelines
├── airflow/dags/               # Airflow DAGs
├── config/                     # Environment configurations
├── data/                       # Data storage
├── db/                         # Database schemas and migrations
├── docker/                     # Docker configurations
├── docs/                       # Documentation
├── kafka_producers/            # Kafka producer applications
├── monitoring/                 # Monitoring configurations
├── scripts/                    # Utility scripts
├── spark_jobs/                 # Spark processing jobs
└── tests/                      # Test suites
```

## 🛠️ Development

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Git

### Setup

1. **Install dependencies**
   ```bash
   ./scripts/setup/install_dependencies.sh
   ```

2. **Configure environment**
   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your settings
   ```

3. **Start services**
   ```bash
   docker-compose up -d
   ```

### Testing

```bash
# Run all tests
make test

# Run specific test suites
make test-unit
make test-integration
```

### Monitoring

```bash
# Start monitoring stack
./scripts/monitoring/start_monitoring.sh

# Access monitoring dashboards
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## 📚 Documentation

- [Architecture](docs/architecture.md) - System architecture overview
- [Setup Guide](docs/setup.md) - Detailed setup instructions
- [Deployment](docs/deployment.md) - Production deployment guide

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the troubleshooting guide

## 🔄 CI/CD

The project includes automated CI/CD pipelines:
- **CI**: Automated testing on pull requests
- **CD**: Automated deployment to staging/production
- **Docker Build**: Container image building and pushing

## 📊 Monitoring

The pipeline includes comprehensive monitoring:
- System metrics (CPU, memory, disk)
- Application metrics (Kafka lag, Spark job duration)
- Business metrics (data processing volume, error rates)
- Custom dashboards and alerts
