""""
This module contains function to transform XML to JSON.
"""

# Import modules
import json
import os
import xml.etree.ElementTree as ET
from operations import logger
from dotenv import load_dotenv
# Loading up the env file values
load_dotenv()


tags = ["item", "category", "description", "image", "price", "prices",
        "currency", "value", "id", "images"]


def xml_to_json(file, file_name):
    """
    This function is used to convert xml file to json output
    :param file_name: name of the file
    :param file: Input file from s3 bucket
    :return: Boolean value and new file name
    """
    path_to_upload_file = None
    output = {}
    list_output = []
    output["Prices"] = []
    try:
        tree = ET.parse(file)
        root = tree.getroot()
        # Iterating over root to get all child
        for child in root:
            if 'id' in output:
                logger.info('Checking id in output variable dictionary')
                output = {"Prices": []}
            if 'id' in child.attrib:
                logger.info('Checking id in child attribute')
                output['product_id'] = child.attrib['id']
            if len(child) > 0:
                for sub_child in child:
                    if sub_child.tag.split('}')[1] == 'prices':
                        for inner_child in sub_child:
                            price_dict = {}
                            count = 0
                            if inner_child.tag.split('}')[1] == 'price':
                                for deep in inner_child:
                                    ref_name = deep.tag.split('}')[1]
                                    ref_val = deep.text
                                    price_dict[count] = {ref_name: ref_val}
                                    count = count +1
                                data = {**price_dict[0], **price_dict[1]}
                                logger.info("Inserting prices data in output dictionary")
                                output["Prices"].insert(0, data)
                    elif sub_child.tag.split('}')[1] == 'images':
                        output["product_images"] = {}
                        for inner_child in sub_child:
                            logger.info("Inserting product images in output dictionary")
                            output["product_images"][inner_child.attrib['type']] =\
                                inner_child.attrib['url']
                    elif sub_child.tag.split('}')[1] == 'category':
                        logger.info("Inserting product category in output dictionary")
                        output['product_category'] = sub_child.text
                    elif sub_child.tag.split('}')[1] == 'description':
                        logger.info("Inserting product description in output dictionary")
                        output['product_description'] = sub_child.text
                logger.info("Generating final output list in form of dictionary")
                list_output.append(output)
                converted_file = file_name.split('.')[0]+'.json'
                logger.info("Writing xml data to json file")
                upload_path = os.environ.get('UPLOAD_FILE_PATH')
                path_to_upload_file = upload_path+converted_file
                with open(path_to_upload_file, 'w', encoding='utf-8') as json_file:
                    json.dump(list_output, json_file, ensure_ascii=False, indent=4)
                logger.info("Conversion of XML to Json completed")
    except Exception as error:
        logger.exception("Error occurred while parsing xml file due to %s", error)
        return False
    return True, path_to_upload_file
