"""
This module contains function to monitor AWS S3 bucket for new files continuously
"""

# Import modules
import json
import os
import urllib
from operations import logger, aws_object
from operations.fileop import FileOperations
from transformation.xmtojson import xml_to_json

from dotenv import load_dotenv
# Loading up the values
load_dotenv()

def check_bucket():
    """
    Function to monitor the S3 bucket for new files
    :return: new files or None
    """
    try:
        logger.info('Infinite while loop starting. Press Ctrl-C to terminate')
        resp = None
        sqs_client = aws_object.get_resource("sqsclient")
        while True:
            try:
                resp = sqs_client.receive_message(
                    QueueUrl=os.environ.get('QUEUE_URL'),
                    AttributeNames=['All'],
                    MaxNumberOfMessages=10,
                    WaitTimeSeconds=10,
                )
            except Exception as error:
                logger.exception("Exception occurred while trying to fetch new messages %s", error)

            if 'Messages' not in resp:
                logger.info('No messages found')
                continue

            for message in resp['Messages']:
                body = json.loads(message['Body'])
                try:
                    record = body['Records'][0]
                    event_name = record['eventName']
                except Exception as error:
                    logger.info('Error occurred while reading messages %s but continuing', error)
                    continue

                if event_name.startswith('ObjectCreated'):
                    # new file created!
                    s3_info = record['s3']
                    object_info = s3_info['object']
                    key = urllib.parse.unquote_plus(object_info['key'])
                    logger.info('Found new object %s', key)
                    download_path = os.environ.get('DOWNLOAD_FILE_PATH')
                    file_ops_download = FileOperations(download_path+key,
                                                       os.environ.get('BUCKET_NAME'))
                    status = file_ops_download.download_file(key)
                    if status is not None:
                        converted_file_status = xml_to_json(status, key)
                        if converted_file_status[0]:
                            file_ops_upload = FileOperations(converted_file_status[1],
                                                             os.environ.get('UPLOAD_BUCKET_NAME'))
                            file_ops_upload.upload_file(key.split('.')[0]+'.json')

            # delete messages from the queue
            entries = [
                {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
                for msg in resp['Messages']
            ]

            try:
                resp = sqs_client.delete_message_batch(
                    QueueUrl=os.environ.get('QUEUE_URL'), Entries=entries
                )
            except Exception as error:
                logger.exception("Exception occurred while deleting messages from queue %s", error)

            if len(resp['Successful']) != len(entries):
                logger.info("Failed to delete messages: entries=%s", entries)

    except KeyboardInterrupt:
        logger.info('Ctrl-C caught!')
