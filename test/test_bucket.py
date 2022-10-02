import unittest
from unittest import mock


class TestS3bucket(unittest.TestCase):

    @mock.patch("operations.Bucket.S3bucket.create_bucket")
    @mock.patch("operations.Bucket.S3bucket")
    def test_create_bucket(self, mock_s3class, mock_create_bucket):
        mock_response = {'ResponseMetadata':
                        {
                            'HTTPStatusCode': 200,
                        }}
        mock_create_bucket.return_value = mock_response
        mock_s3class().create_bucket.return_value = 200
        bucket = mock_s3class("test-bucket")
        response = bucket.create_bucket()
        self.assertEqual(mock_response['ResponseMetadata']['HTTPStatusCode'], response)

    @mock.patch("operations.Bucket.S3bucket.configure_notification_system")
    @mock.patch("operations.Bucket.S3bucket")
    def test_configure_notification_system(self, mock_s3class, mock_configuration):
        mock_response = {'ResponseMetadata':
                        {
                            'HTTPStatusCode': 200,
                        }}
        mock_configuration.return_value = mock_response
        mock_s3class().configure_notification_system.return_value = 200
        bucket = mock_s3class("test-bucket")
        response = bucket.configure_notification_system()
        self.assertEqual(mock_response['ResponseMetadata']['HTTPStatusCode'], response)


if __name__ == '__main__':
    unittest.main()