#!/bin/bash

# Database Setup Script
# This script sets up the PostgreSQL database for the data streaming pipeline

set -e

echo "🗄️ Setting up database..."

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
until docker-compose exec postgres pg_isready -U streaming_user -d streaming_db; do
    echo "PostgreSQL is unavailable - sleeping"
    sleep 2
done

echo "✅ PostgreSQL is ready!"

# Run database initialization
echo "🔧 Running database initialization..."
docker-compose exec postgres psql -U streaming_user -d streaming_db -f /docker-entrypoint-initdb.d/init.sql

echo "✅ Database setup completed!"
