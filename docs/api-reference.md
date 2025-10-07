# API Reference

This document provides comprehensive API documentation for the Data Streaming Pipeline.

## Table of Contents

- [Kafka Producers API](#kafka-producers-api)
- [Spark Jobs API](#spark-jobs-api)
- [AWS Integration API](#aws-integration-api)
- [Frontend API](#frontend-api)
- [Data Sources API](#data-sources-api)

## Kafka Producers API

### JSONProducer

A Kafka producer for sending JSON data to Kafka topics.

#### Methods

##### `__init__()`
Initialize the JSON producer.

**Parameters:** None

**Returns:** JSONProducer instance

##### `send_data(data, key=None)`
Send data to Kafka topic.

**Parameters:**
- `data` (dict): Data to send
- `key` (str, optional): Message key

**Returns:** bool - True if successful, False otherwise

**Example:**
```python
producer = JSONProducer()
data = {'id': 1, 'name': 'Test', 'value': 42.5}
success = producer.send_data(data, key='test_key')
```

##### `send_batch(data_list)`
Send multiple messages to Kafka.

**Parameters:**
- `data_list` (list): List of data dictionaries

**Returns:** int - Number of successfully sent messages

**Example:**
```python
producer = JSONProducer()
data_list = [
    {'id': 1, 'name': 'Item 1'},
    {'id': 2, 'name': 'Item 2'}
]
success_count = producer.send_batch(data_list)
```

##### `close()`
Close the producer.

**Parameters:** None

**Returns:** None

### APIProducer

A Kafka producer for fetching data from APIs and sending to Kafka.

#### Methods

##### `__init__(api_url, headers=None)`
Initialize the API producer.

**Parameters:**
- `api_url` (str): Base API URL
- `headers` (dict, optional): HTTP headers

**Returns:** APIProducer instance

##### `fetch_and_send(endpoint='', params=None)`
Fetch data from API and send to Kafka.

**Parameters:**
- `endpoint` (str): API endpoint to fetch from
- `params` (dict): Query parameters

**Returns:** bool - True if successful, False otherwise

**Example:**
```python
producer = APIProducer('https://api.example.com')
success = producer.fetch_and_send('users', {'limit': 10})
```

##### `start_polling(interval=60, endpoint='', params=None)`
Start polling API at regular intervals.

**Parameters:**
- `interval` (int): Polling interval in seconds
- `endpoint` (str): API endpoint
- `params` (dict): Query parameters

**Returns:** None

**Example:**
```python
producer = APIProducer('https://api.example.com')
producer.start_polling(interval=300, endpoint='data')
```

## Spark Jobs API

### StreamingTransformations

Real-time data processing using Apache Spark Streaming.

#### Methods

##### `__init__(kafka_bootstrap_servers='localhost:9092')`
Initialize streaming transformations.

**Parameters:**
- `kafka_bootstrap_servers` (str): Kafka bootstrap servers

**Returns:** StreamingTransformations instance

##### `parse_json_data()`
Parse JSON data from Kafka.

**Returns:** DataFrame - Parsed data

##### `aggregate_data(df, window_duration='5 minutes')`
Aggregate data by time windows.

**Parameters:**
- `df` (DataFrame): Input DataFrame
- `window_duration` (str): Window duration

**Returns:** DataFrame - Aggregated data

##### `enrich_data(df)`
Enrich data with additional fields.

**Parameters:**
- `df` (DataFrame): Input DataFrame

**Returns:** DataFrame - Enriched data

##### `start_streaming()`
Start the streaming job.

**Parameters:** None

**Returns:** None

### BatchTransformations

Batch data processing using Apache Spark.

#### Methods

##### `__init__()`
Initialize batch transformations.

**Returns:** BatchTransformations instance

##### `load_data(table_name, connection_properties)`
Load data from database.

**Parameters:**
- `table_name` (str): Source table name
- `connection_properties` (dict): Database connection properties

**Returns:** DataFrame - Loaded data

##### `calculate_metrics(df)`
Calculate business metrics.

**Parameters:**
- `df` (DataFrame): Input DataFrame

**Returns:** DataFrame - Calculated metrics

##### `detect_anomalies(df, threshold=2.0)`
Detect anomalies in data.

**Parameters:**
- `df` (DataFrame): Input DataFrame
- `threshold` (float): Z-score threshold

**Returns:** DataFrame - Data with anomaly flags

##### `create_summary_report(df)`
Create summary report.

**Parameters:**
- `df` (DataFrame): Input DataFrame

**Returns:** DataFrame - Summary report

## AWS Integration API

### S3BackupManager

Manage PostgreSQL database backups to S3.

#### Methods

##### `__init__()`
Initialize S3 backup manager.

**Returns:** S3BackupManager instance

##### `create_database_backup()`
Create a PostgreSQL database backup.

**Returns:** tuple - (backup_path, backup_filename)

##### `upload_to_s3(local_file_path, s3_key)`
Upload file to S3.

**Parameters:**
- `local_file_path` (str): Local file path
- `s3_key` (str): S3 object key

**Returns:** bool - True if successful

##### `cleanup_old_backups(retention_days=30)`
Clean up old backups from S3.

**Parameters:**
- `retention_days` (int): Retention period in days

**Returns:** None

##### `run_backup()`
Run the complete backup process.

**Returns:** bool - True if successful

### CloudWatchMetricsCollector

Collect and send metrics to CloudWatch.

#### Methods

##### `__init__()`
Initialize CloudWatch metrics collector.

**Returns:** CloudWatchMetricsCollector instance

##### `get_database_metrics()`
Collect database metrics.

**Returns:** dict - Database metrics

##### `get_kafka_metrics()`
Collect Kafka metrics.

**Returns:** dict - Kafka metrics

##### `get_spark_metrics()`
Collect Spark metrics.

**Returns:** dict - Spark metrics

##### `send_metrics_to_cloudwatch(metrics)`
Send metrics to CloudWatch.

**Parameters:**
- `metrics` (dict): Metrics to send

**Returns:** None

##### `create_cloudwatch_alarms()`
Create CloudWatch alarms.

**Returns:** None

## Frontend API

### Next.js API Routes

#### `/api/metrics`
Get real-time metrics data.

**Method:** GET

**Response:**
```json
[
  {
    "timestamp": "2024-01-01T00:00:00Z",
    "value": 120,
    "category": "A"
  }
]
```

#### `/api/status`
Get system status.

**Method:** GET

**Response:**
```json
{
  "kafka": "healthy",
  "spark": "healthy",
  "postgres": "healthy",
  "airflow": "healthy"
}
```

## Data Sources API

### SampleAPIProducer

Fetch data from various APIs and send to Kafka.

#### Methods

##### `fetch_weather_data(city)`
Fetch weather data from OpenWeatherMap API.

**Parameters:**
- `city` (str): City name

**Returns:** dict - Weather data

##### `fetch_stock_data(symbol)`
Fetch stock data from Alpha Vantage API.

**Parameters:**
- `symbol` (str): Stock symbol

**Returns:** dict - Stock data

##### `fetch_ecommerce_data()`
Fetch e-commerce data from JSONPlaceholder API.

**Returns:** list - E-commerce data

### SampleJSONFilesProducer

Read JSON files and send to Kafka.

#### Methods

##### `generate_sample_json_files()`
Generate sample JSON files for testing.

**Returns:** None

##### `read_and_send_json_files()`
Read JSON files and send to Kafka.

**Returns:** None

## Error Handling

All API methods include proper error handling and logging. Errors are logged using the Python logging module and appropriate exceptions are raised.

### Common Exceptions

- `ConnectionError`: Network connection issues
- `ValueError`: Invalid parameter values
- `RuntimeError`: Runtime errors in data processing
- `Exception`: General exceptions

### Error Response Format

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

## Rate Limiting

API calls are subject to rate limiting to prevent abuse:

- Kafka producers: 1000 messages per minute
- API producers: 100 requests per minute
- Database operations: 100 queries per minute

## Authentication

Most APIs require authentication:

- AWS APIs: AWS credentials (access key, secret key)
- Database APIs: Database connection credentials
- External APIs: API keys (OpenWeatherMap, Alpha Vantage)

## Examples

### Complete Data Pipeline Example

```python
from kafka_producers.json_producer import JSONProducer
from spark_jobs.streaming_transformations import StreamingTransformations
from aws.s3_backup_script import S3BackupManager

# Initialize components
producer = JSONProducer()
streaming = StreamingTransformations()
backup_manager = S3BackupManager()

# Send data
data = {'id': 1, 'name': 'Test', 'value': 42.5}
producer.send_data(data)

# Process data
streaming.start_streaming()

# Backup database
backup_manager.run_backup()

# Cleanup
producer.close()
streaming.stop()
```

### Frontend Integration Example

```javascript
// Fetch metrics
const response = await fetch('/api/metrics');
const metrics = await response.json();

// Fetch status
const statusResponse = await fetch('/api/status');
const status = await statusResponse.json();
```
