import requests
import json
import time
import logging
from kafka import KafkaProducer
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIProducer:
    def __init__(self, api_url, headers=None):
        self.api_url = api_url
        self.headers = headers or {}
        self.producer = KafkaProducer(
            bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None
        )
        self.topic = Config.KAFKA_TOPIC_RAW_DATA
    
    def fetch_and_send(self, endpoint='', params=None):
        """
        Fetch data from API and send to Kafka
        
        Args:
            endpoint (str): API endpoint to fetch from
            params (dict): Query parameters
        """
        try:
            url = f"{self.api_url}/{endpoint}" if endpoint else self.api_url
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            # Send to Kafka
            if isinstance(data, list):
                for item in data:
                    self.producer.send(self.topic, value=item)
            else:
                self.producer.send(self.topic, value=data)
            
            self.producer.flush()
            logger.info(f'Successfully fetched and sent data from {url}')
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f'API request failed: {e}')
            return False
        except Exception as e:
            logger.error(f'Error processing API data: {e}')
            return False
    
    def start_polling(self, interval=60, endpoint='', params=None):
        """
        Start polling API at regular intervals
        
        Args:
            interval (int): Polling interval in seconds
            endpoint (str): API endpoint
            params (dict): Query parameters
        """
        logger.info(f'Starting API polling every {interval} seconds')
        
        while True:
            try:
                self.fetch_and_send(endpoint, params)
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info('Stopping API polling')
                break
            except Exception as e:
                logger.error(f'Error in polling loop: {e}')
                time.sleep(interval)
    
    def close(self):
        """Close the producer"""
        self.producer.close()

def main():
    # Example usage
    api_producer = APIProducer(
        api_url='https://jsonplaceholder.typicode.com/posts',
        headers={'User-Agent': 'DataStreamingPipeline/1.0'}
    )
    
    # Fetch and send data once
    api_producer.fetch_and_send()
    
    # Or start continuous polling
    # api_producer.start_polling(interval=300)  # Every 5 minutes
    
    api_producer.close()

if __name__ == '__main__':
    main()
