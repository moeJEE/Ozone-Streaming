import pytest
import os
import tempfile
from unittest.mock import Mock, patch
import json
from datetime import datetime

@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture
def mock_kafka_producer():
    """Mock Kafka producer for testing"""
    with patch('kafka.KafkaProducer') as mock:
        yield mock

@pytest.fixture
def mock_spark_session():
    """Mock Spark session for testing"""
    with patch('pyspark.sql.SparkSession') as mock:
        yield mock

@pytest.fixture
def sample_data():
    """Sample data for testing"""
    return {
        'id': 'test_001',
        'timestamp': '2024-01-01T00:00:00Z',
        'source': 'test_source',
        'value': 42.5,
        'category': 'test_category'
    }

@pytest.fixture
def sample_weather_data():
    """Sample weather data for testing"""
    return {
        'id': 'weather_london_1234567890',
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'openweathermap',
        'data_type': 'weather',
        'city': 'London',
        'temperature': 15.5,
        'humidity': 65,
        'pressure': 1013.25,
        'description': 'clear sky',
        'wind_speed': 3.2,
        'processed': False
    }

@pytest.fixture
def sample_stock_data():
    """Sample stock data for testing"""
    return {
        'id': 'stock_AAPL_1234567890',
        'timestamp': datetime.utcnow().isoformat(),
        'source': 'alphavantage',
        'data_type': 'stock',
        'symbol': 'AAPL',
        'open': 150.25,
        'high': 152.10,
        'low': 149.80,
        'close': 151.50,
        'volume': 1000000,
        'processed': False
    }

@pytest.fixture
def sample_ecommerce_data():
    """Sample e-commerce data for testing"""
    return [
        {
            'id': 'ecommerce_post_1',
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'jsonplaceholder',
            'data_type': 'ecommerce',
            'post_id': 1,
            'user_id': 1,
            'title': 'Sample Product 1',
            'body': 'This is a sample product description',
            'processed': False
        },
        {
            'id': 'ecommerce_post_2',
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'jsonplaceholder',
            'data_type': 'ecommerce',
            'post_id': 2,
            'user_id': 2,
            'title': 'Sample Product 2',
            'body': 'This is another sample product description',
            'processed': False
        }
    ]

@pytest.fixture
def mock_aws_credentials():
    """Mock AWS credentials for testing"""
    with patch.dict(os.environ, {
        'AWS_ACCESS_KEY_ID': 'test_key',
        'AWS_SECRET_ACCESS_KEY': 'test_secret',
        'AWS_DEFAULT_REGION': 'us-west-2'
    }):
        yield

@pytest.fixture
def mock_database_connection():
    """Mock database connection for testing"""
    with patch('psycopg2.connect') as mock:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.return_value = (1,)
        mock_cursor.fetchall.return_value = [(1, 'test', 'data')]
        mock_conn.cursor.return_value = mock_cursor
        mock.return_value = mock_conn
        yield mock_conn

@pytest.fixture
def sample_json_file(temp_dir):
    """Create a sample JSON file for testing"""
    data = [
        {'id': 1, 'name': 'Test Item 1', 'value': 100},
        {'id': 2, 'name': 'Test Item 2', 'value': 200}
    ]
    file_path = os.path.join(temp_dir, 'test_data.json')
    with open(file_path, 'w') as f:
        json.dump(data, f)
    return file_path

@pytest.fixture
def mock_requests_get():
    """Mock requests.get for testing API calls"""
    with patch('requests.get') as mock:
        mock_response = Mock()
        mock_response.json.return_value = {'test': 'data'}
        mock_response.raise_for_status.return_value = None
        mock.return_value = mock_response
        yield mock
