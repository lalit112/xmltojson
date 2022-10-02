"""
This module contains class and methods for handling file operations
"""

# Import modules
import os
from botocore.exceptions import ClientError
from operations import logger, aws_object
from dotenv import load_dotenv
# Loading up the values
load_dotenv()

class FileOperations:
    """
    Class for handling file operations
    """
    def __init__(self, file_name, bucket):
        """
        Class constructor method for initializing variables
        :param file_name: name of file
        :param bucket: S3 bucket name
        """
        self.file = file_name
        self.bucket = bucket

    def upload_file(self, object_name=None):
        """
        Function to upload a file to a S3 bucket.
        :param object_name: File name
        :return: None
        """
        try:
            if object_name is None:
                object_name = os.path.basename(self.file)
            s3_client = aws_object.get_resource("s3client")
            logger.info('Uploading file to S3 bucket.')
            response = s3_client.upload_file(
                self.file, self.bucket, object_name)
            logger.info('File uploaded successfully to S3 bucket.')
        except ClientError:
            logger.exception('Could not upload file to S3 bucket.')
            raise
        else:
            return response, object_name

    def download_file(self, object_name):
        """
        Function to download a file from a S3 bucket.
        :param object_name:path to local system to download file
        :return: None
        """
        try:
            s3_resource = aws_object.get_resource()
            logger.info('Downloading file from S3 bucket.')
            s3_resource.Bucket(self.bucket).download_file(object_name, self.file)
            logger.info('File downloaded successfully from s3 bucket')
            return self.file
        except ClientError:
            logger.exception('Could not download file to S3 bucket.')
            return None
