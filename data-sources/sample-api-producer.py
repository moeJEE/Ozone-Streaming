#!/usr/bin/env python3
"""
Sample API Producer for Data Streaming Pipeline
This script demonstrates how to fetch data from various APIs and send to Kafka
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from kafka import KafkaProducer
from typing import Dict, List, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SampleAPIProducer:
    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.topic = os.getenv('KAFKA_TOPIC_RAW_DATA', 'raw_data')
    
    def fetch_weather_data(self, city: str) -> Dict[str, Any]:
        """Fetch weather data from OpenWeatherMap API"""
        api_key = os.getenv('OPENWEATHER_API_KEY')
        if not api_key:
            logger.warning("OpenWeatherMap API key not found, using mock data")
            return self._generate_mock_weather_data(city)
        
        try:
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Transform data for our pipeline
            transformed_data = {
                'id': f"weather_{city}_{int(time.time())}",
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'openweathermap',
                'data_type': 'weather',
                'city': city,
                'temperature': data['main']['temp'],
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'processed': False
            }
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"Failed to fetch weather data for {city}: {e}")
            return self._generate_mock_weather_data(city)
    
    def fetch_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch stock data from Alpha Vantage API"""
        api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        if not api_key:
            logger.warning("Alpha Vantage API key not found, using mock data")
            return self._generate_mock_stock_data(symbol)
        
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_INTRADAY',
                'symbol': symbol,
                'interval': '1min',
                'apikey': api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if 'Error Message' in data:
                logger.error(f"API Error: {data['Error Message']}")
                return self._generate_mock_stock_data(symbol)
            
            # Get the latest data point
            time_series = data.get('Time Series (1min)', {})
            if not time_series:
                return self._generate_mock_stock_data(symbol)
            
            latest_time = max(time_series.keys())
            latest_data = time_series[latest_time]
            
            # Transform data for our pipeline
            transformed_data = {
                'id': f"stock_{symbol}_{int(time.time())}",
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'alphavantage',
                'data_type': 'stock',
                'symbol': symbol,
                'open': float(latest_data['1. open']),
                'high': float(latest_data['2. high']),
                'low': float(latest_data['3. low']),
                'close': float(latest_data['4. close']),
                'volume': int(latest_data['5. volume']),
                'processed': False
            }
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"Failed to fetch stock data for {symbol}: {e}")
            return self._generate_mock_stock_data(symbol)
    
    def fetch_ecommerce_data(self) -> List[Dict[str, Any]]:
        """Fetch e-commerce data from JSONPlaceholder API"""
        try:
            url = "https://jsonplaceholder.typicode.com/posts"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            posts = response.json()
            
            # Transform data for our pipeline
            transformed_data = []
            for post in posts[:10]:  # Limit to 10 posts
                transformed_post = {
                    'id': f"ecommerce_post_{post['id']}",
                    'timestamp': datetime.utcnow().isoformat(),
                    'source': 'jsonplaceholder',
                    'data_type': 'ecommerce',
                    'post_id': post['id'],
                    'user_id': post['userId'],
                    'title': post['title'],
                    'body': post['body'],
                    'processed': False
                }
                transformed_data.append(transformed_post)
            
            return transformed_data
            
        except Exception as e:
            logger.error(f"Failed to fetch e-commerce data: {e}")
            return self._generate_mock_ecommerce_data()
    
    def _generate_mock_weather_data(self, city: str) -> Dict[str, Any]:
        """Generate mock weather data"""
        import random
        
        return {
            'id': f"weather_{city}_{int(time.time())}",
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'mock_weather',
            'data_type': 'weather',
            'city': city,
            'temperature': round(random.uniform(-10, 35), 1),
            'humidity': random.randint(30, 90),
            'pressure': random.randint(980, 1030),
            'description': random.choice(['clear sky', 'few clouds', 'scattered clouds', 'broken clouds', 'shower rain']),
            'wind_speed': round(random.uniform(0, 20), 1),
            'processed': False
        }
    
    def _generate_mock_stock_data(self, symbol: str) -> Dict[str, Any]:
        """Generate mock stock data"""
        import random
        
        base_price = random.uniform(50, 200)
        
        return {
            'id': f"stock_{symbol}_{int(time.time())}",
            'timestamp': datetime.utcnow().isoformat(),
            'source': 'mock_stock',
            'data_type': 'stock',
            'symbol': symbol,
            'open': round(base_price, 2),
            'high': round(base_price * random.uniform(1.0, 1.05), 2),
            'low': round(base_price * random.uniform(0.95, 1.0), 2),
            'close': round(base_price * random.uniform(0.95, 1.05), 2),
            'volume': random.randint(1000, 100000),
            'processed': False
        }
    
    def _generate_mock_ecommerce_data(self) -> List[Dict[str, Any]]:
        """Generate mock e-commerce data"""
        import random
        
        mock_data = []
        for i in range(10):
            mock_data.append({
                'id': f"ecommerce_mock_{i}",
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'mock_ecommerce',
                'data_type': 'ecommerce',
                'post_id': i + 1,
                'user_id': random.randint(1, 10),
                'title': f"Mock Product {i + 1}",
                'body': f"This is a mock product description for item {i + 1}",
                'processed': False
            })
        
        return mock_data
    
    def send_to_kafka(self, data: Dict[str, Any] | List[Dict[str, Any]]) -> bool:
        """Send data to Kafka"""
        try:
            if isinstance(data, list):
                for item in data:
                    self.kafka_producer.send(
                        self.topic,
                        value=item,
                        key=item.get('id', 'unknown')
                    )
            else:
                self.kafka_producer.send(
                    self.topic,
                    value=data,
                    key=data.get('id', 'unknown')
                )
            
            self.kafka_producer.flush()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send data to Kafka: {e}")
            return False
    
    def run_continuous_ingestion(self, interval: int = 60):
        """Run continuous data ingestion"""
        logger.info(f"Starting continuous data ingestion every {interval} seconds")
        
        cities = ['London', 'New York', 'Tokyo', 'Paris', 'Sydney']
        stock_symbols = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
        
        while True:
            try:
                # Fetch weather data for random cities
                for city in cities[:2]:  # Fetch for 2 cities each cycle
                    weather_data = self.fetch_weather_data(city)
                    self.send_to_kafka(weather_data)
                    logger.info(f"Sent weather data for {city}")
                
                # Fetch stock data for random symbols
                for symbol in stock_symbols[:2]:  # Fetch for 2 symbols each cycle
                    stock_data = self.fetch_stock_data(symbol)
                    self.send_to_kafka(stock_data)
                    logger.info(f"Sent stock data for {symbol}")
                
                # Fetch e-commerce data
                ecommerce_data = self.fetch_ecommerce_data()
                self.send_to_kafka(ecommerce_data)
                logger.info(f"Sent {len(ecommerce_data)} e-commerce records")
                
                # Wait for next cycle
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Stopping data ingestion")
                break
            except Exception as e:
                logger.error(f"Error in continuous ingestion: {e}")
                time.sleep(interval)
    
    def close(self):
        """Close the Kafka producer"""
        self.kafka_producer.close()

def main():
    """Main function"""
    producer = SampleAPIProducer()
    
    try:
        # Run continuous ingestion
        producer.run_continuous_ingestion(interval=30)  # Every 30 seconds
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
