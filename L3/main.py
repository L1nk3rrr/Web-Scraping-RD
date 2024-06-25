import xml.etree.ElementTree as ET

from lxml import html


def parse_xpath_xml():
    tree = ET.parse('../L2/cats.xml')
    root = tree.getroot()
    facts = root.findall('.//fact')
    facts = [fact.text for fact in facts]
    print(facts)

    lengths = root.findall('.//info[2]/length')
    lengths = list(map(lambda length: length.text, lengths))
    print(lengths)

    lengths = root.findall(".//info[@id='info_1']/length")
    lengths = list(map(lambda length: length.text, lengths))
    print(lengths)


def parse_xpath_html():
    tree = html.parse('training.html')
    a_attrib = tree.xpath("//a[@href='#']")
    texts = list(map(lambda tag: tag.text, a_attrib))
    print(texts)


if __name__ == '__main__':

    parse_xpath_xml()
    parse_xpath_html()