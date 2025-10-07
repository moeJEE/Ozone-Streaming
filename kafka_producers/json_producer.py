import json
import time
import logging
from kafka import KafkaProducer
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JSONProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.topic = Config.KAFKA_TOPIC_RAW_DATA
    
    def send_data(self, data, key=None):
        """
        Send data to Kafka topic
        
        Args:
            data (dict): Data to send
            key (str, optional): Message key
        """
        try:
            future = self.producer.send(self.topic, value=data, key=key)
            record_metadata = future.get(timeout=10)
            logger.info(f'Message sent to {record_metadata.topic} partition {record_metadata.partition} offset {record_metadata.offset}')
            return True
        except Exception as e:
            logger.error(f'Error sending message: {e}')
            return False
    
    def send_batch(self, data_list):
        """
        Send multiple messages to Kafka
        
        Args:
            data_list (list): List of data dictionaries
        """
        success_count = 0
        for data in data_list:
            if self.send_data(data):
                success_count += 1
        logger.info(f'Sent {success_count}/{len(data_list)} messages successfully')
        return success_count
    
    def close(self):
        """Close the producer"""
        self.producer.close()

def main():
    producer = JSONProducer()
    
    # Example usage
    sample_data = {
        'id': 1,
        'name': 'Sample Data',
        'timestamp': time.time(),
        'value': 42.5
    }
    
    producer.send_data(sample_data, key='sample_key')
    producer.close()

if __name__ == '__main__':
    main()
