import xml.etree.ElementTree as ET
from pathlib import Path
import json


def parse_xml_1():
    result = []
    file = Path('cats_result.txt')

    tree = ET.parse('cats.xml')
    root = tree.getroot()

    for child in root:
        for grandchild in child:
            if grandchild.tag == "fact":
                result.append(grandchild.text)

    file.write_text('\n'.join(result))


def parse_xml_2_to_json():
    result = []
    file = Path('cats_result.txt')

    tree = ET.parse('cats.xml')
    root = tree.getroot()

    for info in root.findall('info'):
        fact = info.find('fact')
        result.append(fact.text)

    file.write_text('\n'.join(result))


def parse_json_1():
    with open('cats.json') as json_file:
        data = json.load(json_file)

    return data


def parse_xml_2_to_json():
    result_dict = {}

    tree = ET.parse('cats.xml')
    root = tree.getroot()

    for number, info in enumerate(root.findall('info')):
        fact = info.find('fact')
        result_dict[number] = fact.text

    with open('cats_json_result.json', 'w') as json_file:
        json.dump(result_dict, json_file)

    with open('cats_json_result.json', 'r') as json_file:
        read_data = json.load(json_file)

    # keys on json format is stored like strings, not int or smth else
    print(f"{read_data == result_dict=}")

if __name__ == '__main__':
    # parse_xml_1()
    # parse_xml_2()
    # parse_json_1()
    parse_xml_2_to_json()
