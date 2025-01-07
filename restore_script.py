import boto3  # AWS SDK for Python
import os  # For file operations

# Initialize the S3 client
s3 = boto3.client('s3')

# Define the secondary S3 bucket and the restore directory
secondary_bucket = 'prod3-backups-secondary'  # Secondary S3 bucket (cross-region)
restore_dir = '/home/ec2-user/restore'  # Directory to restore files to

def download_from_s3(bucket_name, restore_dir):
    """
    Downloads all files from the specified S3 bucket to a local directory.
    Args:
        bucket_name (str): Name of the S3 bucket.
        restore_dir (str): Local directory where files will be restored.
    """
    try:
        if not os.path.exists(restore_dir):
            os.makedirs(restore_dir)

        response = s3.list_objects_v2(Bucket=bucket_name, Prefix='backups/')
        if 'Contents' in response:
            for obj in response['Contents']:
                s3_key = obj['Key']
                file_name = os.path.basename(s3_key)
                if not file_name:
                    continue

                local_path = os.path.join(restore_dir, file_name)
                s3.download_file(bucket_name, s3_key, local_path)
                print(f"Restored {file_name} to {local_path}")
        else:
            print(f"No files found in bucket {bucket_name} under prefix 'backups/'.")
    except Exception as e:
        print(f"Error during restoration: {e}")

# Restore files from the secondary bucket
download_from_s3(secondary_bucket, restore_dir)
