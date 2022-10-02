import unittest
from unittest import mock


class TestFileOp(unittest.TestCase):

    @mock.patch('operations.FileOp.FileOperations.upload_file')
    @mock.patch('operations.FileOp.FileOperations')
    def test_upload_file(self, mock_class, mock_upload):
        mock_response= None
        mock_upload.return_value = mock_response
        mock_class().upload_file.return_value = None
        operation = mock_class("test.xml", "test")
        response = operation.upload_file()
        self.assertEqual(mock_response, response)

    @mock.patch('operations.FileOp.FileOperations.download_file')
    @mock.patch('operations.FileOp.FileOperations')
    def test_download_file(self, mock_class, mock_download):
        mock_response = None
        mock_download.return_value = mock_response
        mock_class().download_file.return_value = None
        operation = mock_class("test.xml", "test")
        response = operation.download_file()
        self.assertEqual(mock_response, response)



if __name__ == '__main__':
    unittest.main()
