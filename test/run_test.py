import unittest
loader = unittest.TestLoader()
start_dir = 'C:/Users/lalit/PycharmProjects/xmltojson/test'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)