"""
This is the initialization file for keeping the common variables across the project
"""

import configparser
import logging
import sys
import os

from config.awsconfig import AwsConfig

config = configparser.ConfigParser()
config.read('config.ini')

from dotenv import load_dotenv
# Loading up the values
load_dotenv()

aws_object = AwsConfig(os.environ.get('AWS_DEFAULT_REGION'), os.environ.get('AWS_END_POINT_URL'))
# aws_object = AwsConfig(config.get('AWS','aws_region'), config.get('AWS', 'endpoint_url'))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_fmt_long = logging.Formatter(
    fmt='%(asctime)s %(name)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

log_handler_stream = logging.StreamHandler(sys.stdout)
log_handler_stream.setFormatter(log_fmt_long)
log_handler_stream.setLevel(logging.INFO)
logger.addHandler(log_handler_stream)
