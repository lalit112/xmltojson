"""
This module is related to S3 buckets
"""

import os
from botocore.exceptions import ClientError
from operations import aws_object, logger
from .queue import Queue
from dotenv import load_dotenv
# Loading up the values
load_dotenv()

class S3bucket:
    """
    Class for handling buckets
    """
    def __init__(self, bucket_name):
        """
        Method for initializing instance variables
        :param bucket_name: S3 bucket name to be used
        """
        self.bucket = bucket_name

    def create_bucket(self):
        """
        Function to create S3 bucket
        :return: None
        """
        try:
            s3_client = aws_object.get_resource("s3client")
            logger.info('Creating S3 bucket.')
            response = s3_client.create_bucket(
                Bucket=self.bucket)
            logger.info('S3 bucket created successfully')
        except ClientError:
            logger.exception('Could not create S3 bucket locally.')
            raise
        else:
            return response

    def configure_notification_system(self):
        """
        Function to configure notification system to the bucket
        :return: None
        """
        try:
            queue_object = Queue(os.environ.get('QUEUE_NAME'))
            logger.info('Setting bucket notification configuration')
            bucket_notification_config = {
                'QueueConfigurations': [
                    {
                        'QueueArn': queue_object.get_queue_arn(),
                        'Events': [
                            's3:ObjectCreated:*',
                        ]
                    }
                ],
            }
            s3_client = aws_object.get_resource("s3client")
            logger.info('Applying notification to bucket')
            s3_client.put_bucket_notification_configuration(
                Bucket=self.bucket,
                NotificationConfiguration=bucket_notification_config
            )
        except Exception as error:
            logger.exception('could not set bucket notification configuration'
                             'due to error: %s', error)
