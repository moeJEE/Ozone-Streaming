import pytest
from unittest.mock import Mock, patch
import boto3
from aws.s3_backup_script import S3BackupManager
from aws.cloudwatch_metrics import CloudWatchMetricsCollector

class TestS3BackupManager:
    def test_init(self, mock_aws_credentials):
        manager = S3BackupManager()
        assert manager.bucket_name == 'data-streaming-pipeline-backups'
        assert 'host' in manager.db_config
        assert 'port' in manager.db_config
    
    @patch('subprocess.run')
    def test_create_database_backup(self, mock_run, mock_aws_credentials, mock_database_connection):
        mock_run.return_value = Mock(returncode=0, stderr='')
        
        manager = S3BackupManager()
        backup_path, backup_filename = manager.create_database_backup()
        
        assert backup_path.endswith('.sql')
        assert 'postgres_backup_' in backup_filename
        mock_run.assert_called_once()
    
    @patch('boto3.client')
    def test_upload_to_s3(self, mock_boto_client, mock_aws_credentials):
        mock_s3 = Mock()
        mock_boto_client.return_value = mock_s3
        
        manager = S3BackupManager()
        result = manager.upload_to_s3('/tmp/test.sql', 'backups/test.sql')
        
        assert result is True
        mock_s3.upload_file.assert_called_once()
    
    @patch('boto3.client')
    def test_cleanup_old_backups(self, mock_boto_client, mock_aws_credentials):
        mock_s3 = Mock()
        mock_s3.list_objects_v2.return_value = {'Contents': []}
        mock_boto_client.return_value = mock_s3
        
        manager = S3BackupManager()
        manager.cleanup_old_backups()
        
        mock_s3.list_objects_v2.assert_called_once()

class TestCloudWatchMetricsCollector:
    def test_init(self, mock_aws_credentials):
        collector = CloudWatchMetricsCollector()
        assert collector.namespace == 'DataStreamingPipeline'
        assert 'host' in collector.db_config
    
    @patch('psycopg2.connect')
    def test_get_database_metrics(self, mock_connect, mock_aws_credentials):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_cursor.fetchone.side_effect = [(5,), (1024000,), (10,), (100, 50, 25)]
        mock_cursor.fetchall.return_value = [('table1', 10, 5, 2)]
        mock_conn.cursor.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        
        collector = CloudWatchMetricsCollector()
        metrics = collector.get_database_metrics()
        
        assert 'database_connections' in metrics
        assert 'database_size_bytes' in metrics
        assert 'total_records' in metrics
        assert 'processed_records' in metrics
        assert 'processing_rate' in metrics
    
    def test_get_kafka_metrics(self, mock_aws_credentials):
        collector = CloudWatchMetricsCollector()
        metrics = collector.get_kafka_metrics()
        
        assert 'kafka_messages_per_second' in metrics
        assert 'kafka_consumer_lag' in metrics
        assert 'kafka_producer_throughput' in metrics
    
    def test_get_spark_metrics(self, mock_aws_credentials):
        collector = CloudWatchMetricsCollector()
        metrics = collector.get_spark_metrics()
        
        assert 'spark_jobs_running' in metrics
        assert 'spark_tasks_completed' in metrics
        assert 'spark_executor_memory_used' in metrics
    
    @patch('boto3.client')
    def test_send_metrics_to_cloudwatch(self, mock_boto_client, mock_aws_credentials):
        mock_cloudwatch = Mock()
        mock_boto_client.return_value = mock_cloudwatch
        
        collector = CloudWatchMetricsCollector()
        metrics = {'test_metric': 100, 'another_metric': 200}
        
        collector.send_metrics_to_cloudwatch(metrics)
        
        mock_cloudwatch.put_metric_data.assert_called_once()
        call_args = mock_cloudwatch.put_metric_data.call_args
        assert call_args[1]['Namespace'] == 'DataStreamingPipeline'
        assert len(call_args[1]['MetricData']) == 2
    
    @patch('boto3.client')
    def test_create_cloudwatch_alarms(self, mock_boto_client, mock_aws_credentials):
        mock_cloudwatch = Mock()
        mock_boto_client.return_value = mock_cloudwatch
        
        collector = CloudWatchMetricsCollector()
        collector.create_cloudwatch_alarms()
        
        # Should create 3 alarms
        assert mock_cloudwatch.put_metric_alarm.call_count == 3
