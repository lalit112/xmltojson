"""
This module is the entry point for the application to get started
"""

# Necessary module imports
import os
import time
from operations.bucket import S3bucket
from operations.queue import Queue
from monitoring.monitor import check_bucket
from dotenv import load_dotenv
# Loading up the values
load_dotenv()


# Getting details needed for creation of class objects
s3_bucket = S3bucket(os.environ.get("BUCKET_NAME"))
s3_bucket_upload = S3bucket(os.environ.get('UPLOAD_BUCKET_NAME'))
sns_queue = Queue(os.environ.get('QUEUE_NAME'))

# calling class methods from objects
s3_bucket.create_bucket()
s3_bucket_upload.create_bucket()
sns_queue.create_queue()

# sleep to wait for the queue to be ready
time.sleep(6)

# Applying policy to the queue
sns_queue.set_queue_policy()

# Configuring the notification system on bucket for any incoming files
s3_bucket.configure_notification_system()

# Constantly monitoring bucket for any new files
check_bucket()
