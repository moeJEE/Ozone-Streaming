import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Kafka Configuration
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC_RAW_DATA = os.getenv('KAFKA_TOPIC_RAW_DATA', 'raw_data')
    KAFKA_TOPIC_PROCESSED_DATA = os.getenv('KAFKA_TOPIC_PROCESSED_DATA', 'processed_data')
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://streaming_user:streaming_pass@localhost:5432/streaming_db')
    
    # Spark Configuration
    SPARK_MASTER = os.getenv('SPARK_MASTER', 'spark://localhost:7077')
    SPARK_APP_NAME = os.getenv('SPARK_APP_NAME', 'streaming_pipeline')
    
    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
