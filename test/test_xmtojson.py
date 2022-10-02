import unittest
from unittest import mock
from transformation import xmtojson


class TestXmlTojson(unittest.TestCase):

    @mock.patch('transformation.xmtojson.xml_to_json')
    def test_xml_to_json(self, mock_function):
        mock_function.return_value = [
            {'product_id': 1234,
             'product_category': 'shirts',
             'prices': {'price':[{
                'currency':'SEK',
                'Amount': 1000
             },{
                 'currency': 'EUR',
                 'Amount': 1000

             }]}}]
        input_string = "<nsx:item=1><nsx:category>Jeans</nsx:category>" \
                      "<nsx:description>Bootleg Front Washed</nsx:description><nsx:prices><nsx:price>" \
                      "<nsx:currency>EUR</nsx:currency><nsx:value>1000</nsx:value></nsx:price><nsx:price>" \
                      "<nsx:currency>SEK</nsx:currency><nsx:value>1000</nsx:value></nsx:price></nsx:prices>" \
                      "</nsx:item>"
        response = xmtojson.xml_to_json(input_string, "test.xml")
        self.assertEqual(response, mock_function.return_value)


if __name__ == '__main__':
    unittest.main()
