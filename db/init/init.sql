-- Database initialization script
-- This script sets up the initial database schema

CREATE DATABASE IF NOT EXISTS streaming_db;

-- Create tables for raw data
CREATE TABLE IF NOT EXISTS raw_data (
    id SERIAL PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    source VARCHAR(255),
    processed BOOLEAN DEFAULT FALSE
);

-- Create tables for processed data
CREATE TABLE IF NOT EXISTS processed_data (
    id SERIAL PRIMARY KEY,
    raw_data_id INTEGER REFERENCES raw_data(id),
    processed_data JSONB NOT NULL,
    processing_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_status VARCHAR(50) DEFAULT 'success'
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_raw_data_created_at ON raw_data(created_at);
CREATE INDEX IF NOT EXISTS idx_raw_data_source ON raw_data(source);
CREATE INDEX IF NOT EXISTS idx_processed_data_timestamp ON processed_data(processing_timestamp);

-- Create views for monitoring
CREATE OR REPLACE VIEW data_processing_stats AS
SELECT 
    DATE(created_at) as date,
    source,
    COUNT(*) as total_records,
    COUNT(CASE WHEN processed = TRUE THEN 1 END) as processed_records,
    COUNT(CASE WHEN processed = FALSE THEN 1 END) as pending_records
FROM raw_data
GROUP BY DATE(created_at), source
ORDER BY date DESC, source;

