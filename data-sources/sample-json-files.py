#!/usr/bin/env python3
"""
Sample JSON Files Producer for Data Streaming Pipeline
This script demonstrates how to read JSON files and send to Kafka
"""

import json
import os
import time
import logging
from datetime import datetime
from kafka import KafkaProducer
from typing import Dict, List, Any
from pathlib import Path
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SampleJSONFilesProducer:
    def __init__(self):
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.topic = os.getenv('KAFKA_TOPIC_RAW_DATA', 'raw_data')
        self.data_dir = Path('data-sources/json-files')
        self.data_dir.mkdir(exist_ok=True)
    
    def generate_sample_json_files(self):
        """Generate sample JSON files for testing"""
        logger.info("Generating sample JSON files...")
        
        # Generate user data
        self._generate_user_data()
        
        # Generate product data
        self._generate_product_data()
        
        # Generate transaction data
        self._generate_transaction_data()
        
        # Generate sensor data
        self._generate_sensor_data()
        
        logger.info("Sample JSON files generated successfully")
    
    def _generate_user_data(self):
        """Generate sample user data"""
        users = []
        for i in range(100):
            user = {
                'user_id': f"user_{i+1:03d}",
                'name': f"User {i+1}",
                'email': f"user{i+1}@example.com",
                'age': random.randint(18, 65),
                'city': random.choice(['New York', 'London', 'Tokyo', 'Paris', 'Sydney']),
                'country': random.choice(['US', 'UK', 'JP', 'FR', 'AU']),
                'created_at': datetime.utcnow().isoformat(),
                'is_active': random.choice([True, False])
            }
            users.append(user)
        
        with open(self.data_dir / 'users.json', 'w') as f:
            json.dump(users, f, indent=2)
    
    def _generate_product_data(self):
        """Generate sample product data"""
        products = []
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        
        for i in range(50):
            product = {
                'product_id': f"prod_{i+1:03d}",
                'name': f"Product {i+1}",
                'category': random.choice(categories),
                'price': round(random.uniform(10, 1000), 2),
                'description': f"This is a description for product {i+1}",
                'in_stock': random.choice([True, False]),
                'rating': round(random.uniform(1, 5), 1),
                'created_at': datetime.utcnow().isoformat()
            }
            products.append(product)
        
        with open(self.data_dir / 'products.json', 'w') as f:
            json.dump(products, f, indent=2)
    
    def _generate_transaction_data(self):
        """Generate sample transaction data"""
        transactions = []
        for i in range(200):
            transaction = {
                'transaction_id': f"txn_{i+1:04d}",
                'user_id': f"user_{random.randint(1, 100):03d}",
                'product_id': f"prod_{random.randint(1, 50):03d}",
                'amount': round(random.uniform(10, 500), 2),
                'quantity': random.randint(1, 5),
                'payment_method': random.choice(['credit_card', 'debit_card', 'paypal', 'cash']),
                'status': random.choice(['completed', 'pending', 'failed']),
                'created_at': datetime.utcnow().isoformat()
            }
            transactions.append(transaction)
        
        with open(self.data_dir / 'transactions.json', 'w') as f:
            json.dump(transactions, f, indent=2)
    
    def _generate_sensor_data(self):
        """Generate sample sensor data"""
        sensors = []
        sensor_types = ['temperature', 'humidity', 'pressure', 'light', 'motion']
        
        for i in range(1000):
            sensor_type = random.choice(sensor_types)
            sensor = {
                'sensor_id': f"sensor_{i+1:04d}",
                'sensor_type': sensor_type,
                'location': f"room_{random.randint(1, 10)}",
                'value': self._generate_sensor_value(sensor_type),
                'unit': self._get_sensor_unit(sensor_type),
                'timestamp': datetime.utcnow().isoformat(),
                'battery_level': random.randint(20, 100)
            }
            sensors.append(sensor)
        
        with open(self.data_dir / 'sensors.json', 'w') as f:
            json.dump(sensors, f, indent=2)
    
    def _generate_sensor_value(self, sensor_type: str) -> float:
        """Generate appropriate sensor value based on type"""
        if sensor_type == 'temperature':
            return round(random.uniform(-10, 40), 1)
        elif sensor_type == 'humidity':
            return round(random.uniform(30, 90), 1)
        elif sensor_type == 'pressure':
            return round(random.uniform(980, 1030), 1)
        elif sensor_type == 'light':
            return round(random.uniform(0, 1000), 1)
        elif sensor_type == 'motion':
            return random.choice([0, 1])
        else:
            return round(random.uniform(0, 100), 1)
    
    def _get_sensor_unit(self, sensor_type: str) -> str:
        """Get appropriate unit for sensor type"""
        units = {
            'temperature': '°C',
            'humidity': '%',
            'pressure': 'hPa',
            'light': 'lux',
            'motion': 'binary'
        }
        return units.get(sensor_type, 'unit')
    
    def read_and_send_json_files(self):
        """Read JSON files and send to Kafka"""
        logger.info("Reading JSON files and sending to Kafka...")
        
        json_files = list(self.data_dir.glob('*.json'))
        
        for json_file in json_files:
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
                
                # Transform data for our pipeline
                transformed_data = self._transform_data(data, json_file.stem)
                
                # Send to Kafka
                self.send_to_kafka(transformed_data)
                
                logger.info(f"Sent {len(transformed_data)} records from {json_file.name}")
                
            except Exception as e:
                logger.error(f"Failed to process {json_file.name}: {e}")
    
    def _transform_data(self, data: List[Dict], data_type: str) -> List[Dict]:
        """Transform data for the pipeline"""
        transformed = []
        
        for item in data:
            transformed_item = {
                'id': f"{data_type}_{item.get('id', 'unknown')}_{int(time.time())}",
                'timestamp': datetime.utcnow().isoformat(),
                'source': 'json_files',
                'data_type': data_type,
                'original_data': item,
                'processed': False
            }
            transformed.append(transformed_item)
        
        return transformed
    
    def send_to_kafka(self, data: List[Dict[str, Any]]) -> bool:
        """Send data to Kafka"""
        try:
            for item in data:
                self.kafka_producer.send(
                    self.topic,
                    value=item,
                    key=item.get('id', 'unknown')
                )
            
            self.kafka_producer.flush()
            return True
            
        except Exception as e:
            logger.error(f"Failed to send data to Kafka: {e}")
            return False
    
    def run_continuous_ingestion(self, interval: int = 60):
        """Run continuous data ingestion from JSON files"""
        logger.info(f"Starting continuous JSON file ingestion every {interval} seconds")
        
        # Generate sample files if they don't exist
        if not list(self.data_dir.glob('*.json')):
            self.generate_sample_json_files()
        
        while True:
            try:
                self.read_and_send_json_files()
                time.sleep(interval)
                
            except KeyboardInterrupt:
                logger.info("Stopping JSON file ingestion")
                break
            except Exception as e:
                logger.error(f"Error in continuous ingestion: {e}")
                time.sleep(interval)
    
    def close(self):
        """Close the Kafka producer"""
        self.kafka_producer.close()

def main():
    """Main function"""
    producer = SampleJSONFilesProducer()
    
    try:
        # Generate sample files
        producer.generate_sample_json_files()
        
        # Run continuous ingestion
        producer.run_continuous_ingestion(interval=30)  # Every 30 seconds
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
