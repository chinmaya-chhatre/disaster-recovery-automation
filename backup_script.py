import boto3  # AWS SDK for Python
import os  # For file and directory operations
from datetime import datetime  # To add timestamps to backup files

# Initialize the S3 client
s3 = boto3.client('s3')

# Define S3 bucket names and the backup directory
primary_bucket = 'prod3-backups'  # Primary S3 bucket
secondary_bucket = 'prod3-backups-secondary'  # Secondary S3 bucket (cross-region)
backup_dir = '/home/ec2-user/backup'  # Path to the directory containing files to back up

def upload_to_s3(file_path, bucket_name):
    """
    Uploads a single file to the specified S3 bucket.
    Args:
        file_path (str): Full path of the file to upload.
        bucket_name (str): Name of the S3 bucket where the file will be uploaded.
    """
    try:
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        s3_key = f'backups/{timestamp}_{file_name}'
        s3.upload_file(file_path, bucket_name, s3_key)
        print(f"Uploaded {file_name} to {bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading {file_name} to {bucket_name}: {e}")

# Backup files to both buckets
if os.path.exists(backup_dir):
    for file in os.listdir(backup_dir):
        file_path = os.path.join(backup_dir, file)
        if os.path.isfile(file_path):
            upload_to_s3(file_path, primary_bucket)  # Backup to primary bucket
            upload_to_s3(file_path, secondary_bucket)  # Backup to secondary bucket
else:
    print(f"Backup directory {backup_dir} does not exist.")
