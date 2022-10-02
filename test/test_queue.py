import unittest
from unittest import mock


class TestQueue(unittest.TestCase):

    @mock.patch("operations.Queue.Queue.create_queue")
    @mock.patch("operations.Queue.Queue")
    def test_create_queue(self, mock_class, mock_queue):
        mock_response = {'ResponseMetadata':
                        {
                            'HTTPStatusCode': 200,
                        }}
        mock_queue.return_value = mock_response
        mock_class().create_queue.return_value = 200
        queue = mock_class("test-queue")
        response = queue.create_queue()
        self.assertEqual(mock_response['ResponseMetadata']['HTTPStatusCode'], response)

    @mock.patch("operations.Queue.Queue.get_queue_arn")
    @mock.patch("operations.Queue.Queue")
    def test_get_queue_arn(self, mock_class, mock_queue):
        mock_response = 'arn:aws:sqs:us-east-1:000000000000:abcd'
        mock_queue.return_value = mock_response
        mock_class().get_queue_arn.return_value = "arn:aws:sqs:us-east-1:000000000000:abcd"
        queue = mock_class("test-queue")
        response = queue.get_queue_arn()
        self.assertEqual(mock_response, response)

    @mock.patch("operations.Queue.Queue.set_queue_policy")
    @mock.patch("operations.Queue.Queue")
    def test_set_queue_policy(self, mock_class, mock_queue):
        mock_response = {'ResponseMetadata':
            {
                'HTTPStatusCode': 200,
            }}
        mock_queue.return_value = mock_response
        mock_class().set_queue_policy.return_value = 200
        queue = mock_class("test-queue")
        response = queue.set_queue_policy()
        self.assertEqual(mock_response['ResponseMetadata']['HTTPStatusCode'], response)


if __name__ == '__main__':
    unittest.main()
