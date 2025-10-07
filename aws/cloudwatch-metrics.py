#!/usr/bin/env python3
"""
AWS CloudWatch Metrics Collection Script
This script collects and sends custom metrics to CloudWatch
"""

import boto3
import psycopg2
import json
import time
import logging
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CloudWatchMetricsCollector:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.namespace = 'DataStreamingPipeline'
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'streaming_db'),
            'user': os.getenv('POSTGRES_USER', 'streaming_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'streaming_pass')
        }
    
    def get_database_metrics(self):
        """Collect database metrics"""
        metrics = {}
        
        try:
            conn = psycopg2.connect(**self.db_config)
            cursor = conn.cursor()
            
            # Get connection count
            cursor.execute("SELECT count(*) FROM pg_stat_activity;")
            metrics['database_connections'] = cursor.fetchone()[0]
            
            # Get database size
            cursor.execute("SELECT pg_database_size(current_database());")
            metrics['database_size_bytes'] = cursor.fetchone()[0]
            
            # Get table row counts
            cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    n_tup_ins as inserts,
                    n_tup_upd as updates,
                    n_tup_del as deletes
                FROM pg_stat_user_tables
                ORDER BY n_tup_ins DESC;
            """)
            
            table_stats = cursor.fetchall()
            metrics['table_operations'] = len(table_stats)
            
            # Get recent data processing metrics
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_records,
                    COUNT(CASE WHEN processed = true THEN 1 END) as processed_records,
                    COUNT(CASE WHEN created_at > NOW() - INTERVAL '1 hour' THEN 1 END) as recent_records
                FROM raw_data;
            """)
            
            processing_stats = cursor.fetchone()
            metrics['total_records'] = processing_stats[0]
            metrics['processed_records'] = processing_stats[1]
            metrics['recent_records'] = processing_stats[2]
            
            # Calculate processing rate
            if processing_stats[0] > 0:
                metrics['processing_rate'] = (processing_stats[1] / processing_stats[0]) * 100
            else:
                metrics['processing_rate'] = 0
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            logger.error(f"Failed to collect database metrics: {e}")
            metrics['database_error'] = 1
        
        return metrics
    
    def get_kafka_metrics(self):
        """Collect Kafka metrics (mock implementation)"""
        # In a real implementation, you would connect to Kafka and collect metrics
        # For now, we'll return mock data
        return {
            'kafka_messages_per_second': 150.5,
            'kafka_consumer_lag': 25,
            'kafka_producer_throughput': 1200.0
        }
    
    def get_spark_metrics(self):
        """Collect Spark metrics (mock implementation)"""
        # In a real implementation, you would connect to Spark and collect metrics
        return {
            'spark_jobs_running': 2,
            'spark_tasks_completed': 1250,
            'spark_executor_memory_used': 0.75
        }
    
    def send_metrics_to_cloudwatch(self, metrics):
        """Send metrics to CloudWatch"""
        try:
            metric_data = []
            
            for metric_name, value in metrics.items():
                if isinstance(value, (int, float)):
                    metric_data.append({
                        'MetricName': metric_name,
                        'Value': float(value),
                        'Unit': 'Count',
                        'Timestamp': datetime.utcnow(),
                        'Dimensions': [
                            {
                                'Name': 'Environment',
                                'Value': os.getenv('ENVIRONMENT', 'development')
                            },
                            {
                                'Name': 'Service',
                                'Value': 'DataStreamingPipeline'
                            }
                        ]
                    })
            
            if metric_data:
                self.cloudwatch.put_metric_data(
                    Namespace=self.namespace,
                    MetricData=metric_data
                )
                logger.info(f"Sent {len(metric_data)} metrics to CloudWatch")
            
        except ClientError as e:
            logger.error(f"Failed to send metrics to CloudWatch: {e}")
            raise
    
    def create_cloudwatch_alarms(self):
        """Create CloudWatch alarms for monitoring"""
        alarms = [
            {
                'AlarmName': f'{self.namespace}-HighDatabaseConnections',
                'MetricName': 'database_connections',
                'Namespace': self.namespace,
                'Statistic': 'Average',
                'Period': 300,
                'EvaluationPeriods': 2,
                'Threshold': 80,
                'ComparisonOperator': 'GreaterThanThreshold',
                'AlarmDescription': 'Database connection count is too high'
            },
            {
                'AlarmName': f'{self.namespace}-LowProcessingRate',
                'MetricName': 'processing_rate',
                'Namespace': self.namespace,
                'Statistic': 'Average',
                'Period': 300,
                'EvaluationPeriods': 3,
                'Threshold': 90,
                'ComparisonOperator': 'LessThanThreshold',
                'AlarmDescription': 'Data processing rate is too low'
            },
            {
                'AlarmName': f'{self.namespace}-HighKafkaLag',
                'MetricName': 'kafka_consumer_lag',
                'Namespace': self.namespace,
                'Statistic': 'Average',
                'Period': 300,
                'EvaluationPeriods': 2,
                'Threshold': 100,
                'ComparisonOperator': 'GreaterThanThreshold',
                'AlarmDescription': 'Kafka consumer lag is too high'
            }
        ]
        
        for alarm_config in alarms:
            try:
                self.cloudwatch.put_metric_alarm(**alarm_config)
                logger.info(f"Created alarm: {alarm_config['AlarmName']}")
            except ClientError as e:
                logger.error(f"Failed to create alarm {alarm_config['AlarmName']}: {e}")
    
    def collect_and_send_metrics(self):
        """Collect all metrics and send to CloudWatch"""
        try:
            logger.info("Collecting metrics...")
            
            # Collect metrics from different sources
            db_metrics = self.get_database_metrics()
            kafka_metrics = self.get_kafka_metrics()
            spark_metrics = self.get_spark_metrics()
            
            # Combine all metrics
            all_metrics = {**db_metrics, **kafka_metrics, **spark_metrics}
            
            # Send to CloudWatch
            self.send_metrics_to_cloudwatch(all_metrics)
            
            logger.info("Metrics collection and sending completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to collect and send metrics: {e}")
            return False

def main():
    """Main function"""
    collector = CloudWatchMetricsCollector()
    
    # Collect and send metrics
    success = collector.collect_and_send_metrics()
    
    # Create alarms (only run once)
    if os.getenv('CREATE_ALARMS', 'false').lower() == 'true':
        collector.create_cloudwatch_alarms()
    
    if success:
        print("✅ Metrics collection completed successfully")
        exit(0)
    else:
        print("❌ Metrics collection failed")
        exit(1)

if __name__ == "__main__":
    import os
    main()
