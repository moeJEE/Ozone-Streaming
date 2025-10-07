#!/bin/bash

# Kafka Setup Script
# This script sets up Kafka topics for the data streaming pipeline

set -e

echo "🚀 Setting up Kafka..."

# Wait for Kafka to be ready
echo "⏳ Waiting for Kafka to be ready..."
until docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list; do
    echo "Kafka is unavailable - sleeping"
    sleep 2
done

echo "✅ Kafka is ready!"

# Create topics
echo "📝 Creating Kafka topics..."

# Raw data topic
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic raw_data --partitions 3 --replication-factor 1

# Processed data topic
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic processed_data --partitions 3 --replication-factor 1

# Monitoring topic
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --create --topic monitoring --partitions 1 --replication-factor 1

# List topics
echo "📋 Created topics:"
docker-compose exec kafka kafka-topics --bootstrap-server localhost:9092 --list

echo "✅ Kafka setup completed!"
