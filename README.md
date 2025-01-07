# Disaster Recovery Automation

This project showcases a custom disaster recovery solution that leverages **AWS S3** for file-level backups and cross-region replication. It includes scripts for automating backups and restorations with granular control over data. The solution is designed to complement AWS Backup by offering additional flexibility, cost-efficiency, and cross-region redundancy.

---

## **Why Use This Script Instead of AWS Backup?**

- **Cross-Region Replication:** Automatically replicates data to a secondary S3 bucket in another AWS region for added resilience.
- **Lower Costs:** Focuses on file-level backups instead of full-volume snapshots, reducing storage and transfer costs.
- **Granular Control:** Allows you to specify exactly which files or directories to back up, making it ideal for applications that don't require full-drive recovery.

---

## **Features**

1. **Backup Script:**
   - Uploads files to a primary S3 bucket.
   - Replicates files to a secondary S3 bucket in another region.
   - Includes timestamps in file names for versioning.

2. **Restoration Script:**
   - Restores files from the secondary S3 bucket to an EC2 instance.
   - Ensures recovery even if the primary bucket is unavailable.

3. **Key Benefits:**
   - Simple and cost-effective disaster recovery.
   - Compatible with any Linux environment.

---

## **Setup and Usage**

### Prerequisites
- An AWS account with access to **S3** and **IAM**.
- An EC2 instance running **Amazon Linux 2** or similar.
- Python 3 and the `boto3` library installed.

### Configuration
1. Create two S3 buckets:
   - Primary bucket (e.g., `prod3-backups`).
   - Secondary bucket in a different region (e.g., `prod3-backups-secondary`).

2. Attach an IAM role to the EC2 instance with permissions for S3:
   - Actions: `s3:PutObject`, `s3:GetObject`, `s3:ListBucket`.

3. Set the bucket names and directory paths in the scripts.

---

## **Running the Scripts**

### Backup Script
Run the backup script to upload files to both primary and secondary S3 buckets:
```bash
python3 backup_script.py
```

### Restoration Script
Run the restoration script to download files from the secondary S3 bucket to the EC2 instance:
```bash
python3 restore_script.py
```

---

## **Testing Steps**

Follow these steps to verify that the scripts work as expected:

1. **Test the Backup Script:**
   - Add test files to the backup directory on the EC2 instance:
     ```bash
     mkdir -p /home/ec2-user/backup
     echo "Test file 1" > /home/ec2-user/backup/test1.txt
     echo "Test file 2" > /home/ec2-user/backup/test2.txt
     ```
   - Run the backup script:
     ```bash
     python3 backup_script.py
     ```
   - Verify the files are uploaded to both S3 buckets:
     - Check the `backups/` folder in the primary bucket (`prod3-backups`).
     - Check the `backups/` folder in the secondary bucket (`prod3-backups-secondary`).

2. **Test the Restoration Script:**
   - Ensure the `restore/` directory exists on the EC2 instance:
     ```bash
     mkdir -p /home/ec2-user/restore
     ```
   - Run the restoration script:
     ```bash
     python3 restore_script.py
     ```
   - Verify that the files are restored to `/home/ec2-user/restore` on the EC2 instance.

3. **Cross-Region Verification:**
   - Modify the IAM role or permissions to simulate primary bucket unavailability.
   - Delete files from the primary bucket manually.
   - Run the restoration script to ensure files are restored from the secondary bucket.

---

## **Future Improvements**
- Add notifications (e.g., email or Slack) for backup and restoration events.
- Schedule periodic backups using `cron`.
- Integrate with AWS S3 lifecycle policies for cost optimization.

---

## **License**
This project is open-source and available under the MIT License.
