#!/usr/bin/env python3
"""
AWS S3 Backup Script for PostgreSQL Database
This script creates automated backups of the PostgreSQL database to S3
"""

import boto3
import psycopg2
import os
import subprocess
import logging
from datetime import datetime
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3BackupManager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = os.getenv('S3_BACKUP_BUCKET', 'data-streaming-pipeline-backups')
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'streaming_db'),
            'user': os.getenv('POSTGRES_USER', 'streaming_user'),
            'password': os.getenv('POSTGRES_PASSWORD', 'streaming_pass')
        }
    
    def create_database_backup(self):
        """Create a PostgreSQL database backup"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f"postgres_backup_{timestamp}.sql"
        backup_path = f"/tmp/{backup_filename}"
        
        try:
            # Create pg_dump command
            cmd = [
                'pg_dump',
                '-h', self.db_config['host'],
                '-p', str(self.db_config['port']),
                '-U', self.db_config['user'],
                '-d', self.db_config['database'],
                '-f', backup_path,
                '--verbose'
            ]
            
            # Set password via environment variable
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_config['password']
            
            # Execute backup
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode != 0:
                raise Exception(f"pg_dump failed: {result.stderr}")
            
            logger.info(f"Database backup created: {backup_path}")
            return backup_path, backup_filename
            
        except Exception as e:
            logger.error(f"Failed to create database backup: {e}")
            raise
    
    def upload_to_s3(self, local_file_path, s3_key):
        """Upload file to S3"""
        try:
            self.s3_client.upload_file(
                local_file_path,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ServerSideEncryption': 'AES256',
                    'StorageClass': 'STANDARD_IA'  # Cost-effective for backups
                }
            )
            logger.info(f"File uploaded to S3: s3://{self.bucket_name}/{s3_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to upload to S3: {e}")
            raise
    
    def cleanup_old_backups(self, retention_days=30):
        """Clean up old backups from S3"""
        try:
            # List objects in the backup folder
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix='postgres_backups/'
            )
            
            if 'Contents' not in response:
                logger.info("No backups found to clean up")
                return
            
            # Calculate cutoff date
            cutoff_date = datetime.now().timestamp() - (retention_days * 24 * 60 * 60)
            
            # Delete old backups
            objects_to_delete = []
            for obj in response['Contents']:
                if obj['LastModified'].timestamp() < cutoff_date:
                    objects_to_delete.append({'Key': obj['Key']})
            
            if objects_to_delete:
                self.s3_client.delete_objects(
                    Bucket=self.bucket_name,
                    Delete={'Objects': objects_to_delete}
                )
                logger.info(f"Deleted {len(objects_to_delete)} old backup files")
            
        except ClientError as e:
            logger.error(f"Failed to cleanup old backups: {e}")
            raise
    
    def run_backup(self):
        """Run the complete backup process"""
        try:
            logger.info("Starting database backup process...")
            
            # Create database backup
            backup_path, backup_filename = self.create_database_backup()
            
            # Upload to S3
            s3_key = f"postgres_backups/{backup_filename}"
            self.upload_to_s3(backup_path, s3_key)
            
            # Clean up local file
            os.remove(backup_path)
            logger.info("Local backup file cleaned up")
            
            # Clean up old backups
            self.cleanup_old_backups()
            
            logger.info("Backup process completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Backup process failed: {e}")
            return False

def main():
    """Main function"""
    backup_manager = S3BackupManager()
    success = backup_manager.run_backup()
    
    if success:
        print("✅ Database backup completed successfully")
        exit(0)
    else:
        print("❌ Database backup failed")
        exit(1)

if __name__ == "__main__":
    main()
