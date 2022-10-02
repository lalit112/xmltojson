"""
This module contains configuration methods related to sqs queue in AWS
"""

# Import modules
import os
import json
from operations import aws_object, logger


class Queue:
    """
    Class for handling queue in AWS
    """
    def __init__(self, queue_name):
        """
        Methos for initializing instance variables
        :param queue_name: name of the queue to be used
        """
        self.queue = queue_name

    def create_queue(self):
        """
        Function to create sqs queue in AWS
        :return: Boolean value
        """
        try:
            logger.info('Creating queue %s', self.queue)
            sqs_client = aws_object.get_resource("sqsclient")
            sqs_client.create_queue(QueueName=self.queue)
            return True
        except Exception as error:
            logger.exception('Could not create queue error %s', error)
            return False

    def get_queue_arn(self):
        """
        Function to return the ARN for queue
        :return: queue arn value or None
        """
        try:
            sqs_client = aws_object.get_resource("sqsclient")
            logger.info('Getting queue arn for %s', self.queue)
            queue_arn = sqs_client.get_queue_attributes(
                QueueUrl=os.environ.get('QUEUE_URL'), AttributeNames=
                ['QueueArn'])['Attributes']['QueueArn']
            return queue_arn
        except Exception as error:
            logger.exception('Could not get queue arn due to error %s', error)
            return None

    def set_queue_policy(self):
        """
        Function to set the policy on the AWS queue
        :return: None
        """
        sqs_policy = {
            "Version": "2012-10-17",
            "Id": "example-ID",
            "Statement": [
                {
                    "Sid": "Monitor-SQS-ID",
                    "Effect": "Allow",
                    "Principal": {
                        "AWS": "*"
                    },
                    "Action": [
                        "SQS:SendMessage"
                    ],
                    "Resource": self.get_queue_arn(),
                    "Condition": {
                        "ArnLike": {
                            "aws:SourceArn": f"arn:aws:s3:*:*:{os.environ.get('BUCKET_NAME')}"
                        },
                    }
                }
            ]
        }
        try:
            logger.info('Setting queue attributes')
            sqs_client = aws_object.get_resource("sqsclient")
            sqs_client.set_queue_attributes(
                QueueUrl=os.environ.get('QUEUE_URL'),
                Attributes={
                    'Policy': json.dumps(sqs_policy),
                }
            )
        except Exception as error:
            logger.exception('could not set queue attributes error: %s', error)
