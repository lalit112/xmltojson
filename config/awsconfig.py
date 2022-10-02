"""
This module contains all the configurations needed for AWS resources.
"""

# Import module
import boto3


class AwsConfig:
    """
    Class for managing S3 configuration
    """
    def __init__(self, aws_region, endpoint_url):
        """
        Class constructor for initializing instance variables
        :param aws_region: Region in which AWS services are deployed
        :param endpoint_url: URL for hosted services
        """
        self.aws_region = aws_region
        self.endpoint_url = endpoint_url

    def _get_s3_client(self):
        """
        Protected function to return S3 client instance
        :return: boto3 client
        """
        return boto3.client("s3", region_name=self.aws_region, endpoint_url=self.endpoint_url)

    def _get_s3_resource(self):
        """
        Protected function to return S3 resource instance
        :return: boto3 resource
        """
        return boto3.resource("s3", region_name=self.aws_region, endpoint_url=self.endpoint_url)

    def _get_sqs_client(self):
        """
        Protected function to return sqs instance
        :return: boto3 sqs instance
        """
        return boto3.client('sqs', region_name=self.aws_region, endpoint_url=self.endpoint_url)

    def get_resource(self, resource_type=None):
        """
        Public function to get access to different S3 instances
        :param resource_type: type of resource to get the instance
        :return: S3 instance of resource
        """
        if resource_type == "s3client":
            return self._get_s3_client()
        if resource_type == "sqsclient":
            return self._get_sqs_client()
        return self._get_s3_resource()
