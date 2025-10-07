import pytest
from unittest.mock import Mock, patch
from data_sources.sample_api_producer import SampleAPIProducer
from data_sources.sample_json_files import SampleJSONFilesProducer

class TestSampleAPIProducer:
    def test_init(self, mock_kafka_producer):
        producer = SampleAPIProducer()
        assert producer.topic == 'raw_data'
        mock_kafka_producer.assert_called_once()
    
    def test_fetch_weather_data_mock(self, mock_requests_get):
        producer = SampleAPIProducer()
        weather_data = producer.fetch_weather_data('London')
        
        assert weather_data['city'] == 'London'
        assert weather_data['data_type'] == 'weather'
        assert 'temperature' in weather_data
        assert 'humidity' in weather_data
        assert weather_data['processed'] is False
    
    def test_fetch_stock_data_mock(self, mock_requests_get):
        producer = SampleAPIProducer()
        stock_data = producer.fetch_stock_data('AAPL')
        
        assert stock_data['symbol'] == 'AAPL'
        assert stock_data['data_type'] == 'stock'
        assert 'open' in stock_data
        assert 'close' in stock_data
        assert stock_data['processed'] is False
    
    def test_fetch_ecommerce_data(self, mock_requests_get):
        producer = SampleAPIProducer()
        ecommerce_data = producer.fetch_ecommerce_data()
        
        assert isinstance(ecommerce_data, list)
        assert len(ecommerce_data) > 0
        assert ecommerce_data[0]['data_type'] == 'ecommerce'
        assert ecommerce_data[0]['processed'] is False
    
    def test_send_to_kafka_single(self, mock_kafka_producer, sample_weather_data):
        producer = SampleAPIProducer()
        result = producer.send_to_kafka(sample_weather_data)
        
        assert result is True
        producer.kafka_producer.send.assert_called_once()
        producer.kafka_producer.flush.assert_called_once()
    
    def test_send_to_kafka_list(self, mock_kafka_producer, sample_ecommerce_data):
        producer = SampleAPIProducer()
        result = producer.send_to_kafka(sample_ecommerce_data)
        
        assert result is True
        assert producer.kafka_producer.send.call_count == len(sample_ecommerce_data)
        producer.kafka_producer.flush.assert_called_once()

class TestSampleJSONFilesProducer:
    def test_init(self, mock_kafka_producer):
        producer = SampleJSONFilesProducer()
        assert producer.topic == 'raw_data'
        assert producer.data_dir.exists()
        mock_kafka_producer.assert_called_once()
    
    def test_generate_sample_json_files(self, mock_kafka_producer):
        producer = SampleJSONFilesProducer()
        producer.generate_sample_json_files()
        
        # Check if files were created
        assert (producer.data_dir / 'users.json').exists()
        assert (producer.data_dir / 'products.json').exists()
        assert (producer.data_dir / 'transactions.json').exists()
        assert (producer.data_dir / 'sensors.json').exists()
    
    def test_transform_data(self, mock_kafka_producer):
        producer = SampleJSONFilesProducer()
        original_data = [{'id': 1, 'name': 'Test'}]
        transformed = producer._transform_data(original_data, 'test_type')
        
        assert len(transformed) == 1
        assert transformed[0]['data_type'] == 'test_type'
        assert transformed[0]['source'] == 'json_files'
        assert transformed[0]['processed'] is False
        assert 'original_data' in transformed[0]
    
    def test_send_to_kafka(self, mock_kafka_producer, sample_ecommerce_data):
        producer = SampleJSONFilesProducer()
        result = producer.send_to_kafka(sample_ecommerce_data)
        
        assert result is True
        assert producer.kafka_producer.send.call_count == len(sample_ecommerce_data)
        producer.kafka_producer.flush.assert_called_once()
    
    def test_generate_sensor_data(self, mock_kafka_producer):
        producer = SampleJSONFilesProducer()
        
        # Test temperature sensor
        temp_value = producer._generate_sensor_value('temperature')
        assert -10 <= temp_value <= 40
        
        # Test humidity sensor
        humidity_value = producer._generate_sensor_value('humidity')
        assert 30 <= humidity_value <= 90
        
        # Test motion sensor
        motion_value = producer._generate_sensor_value('motion')
        assert motion_value in [0, 1]
    
    def test_sensor_units(self, mock_kafka_producer):
        producer = SampleJSONFilesProducer()
        
        assert producer._get_sensor_unit('temperature') == '°C'
        assert producer._get_sensor_unit('humidity') == '%'
        assert producer._get_sensor_unit('pressure') == 'hPa'
        assert producer._get_sensor_unit('light') == 'lux'
        assert producer._get_sensor_unit('motion') == 'binary'
