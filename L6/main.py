import os
import re
import hashlib
import json
from time import perf_counter

import requests
from multiprocessing import Pool
from bs4 import BeautifulSoup


def parse_xml():
    xml = """<?xml version="1.0" encoding=utf-8>
    <library>
        <book>
            <title>The Catcher in the Rye</title>
            <author>J.D. Salinger</author>
            <year>1951</year>
            <isbn>978-0-316-76948-0</isbn>
        </book>
        <book>
            <title>1984</title>
            <author>George Orwell</author>
            <year>1949</year>
            <isbn>978-0-452-28423-4</isbn>
        </book>
        <book>
            <title>To Kill a Mockingbird</title>
            <author>Harper Lee</author>
            <year>1960</year>
            <isbn>978-0-06-112008-4</isbn>
        </book>
    </library>
    """
    soup = BeautifulSoup(xml, features="xml")
    book = soup.find("book")
    print(book)

    harper_string = soup.find(string="Harper Lee")
    print(harper_string)

    title_regexp = soup.find_all('title', string=re.compile('Catcher|1984'))
    print(title_regexp)

    titles = soup.find_all('title')
    titles = [tag.text for tag in titles]

    years = [tag.text for tag in soup.find_all('year')]

    for title, years in zip(titles,years):
        print(f'The book f{title} was written in {years}')

def get_content(url):
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()

    # if os.path.exists(filename):
    #     with open(filename, 'r') as f:
    #         content = f.read()
    #     return content

    response = requests.get(
        url=url,
        headers={
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        }
    )
    content = response.text

    # with open(filename, 'w') as f:
    #     f.write(content)
    return content


def parse_morin():
    data = []
    url = "https://job.morion.ua/jobs/"
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')
    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]
    for block in blocks:
        title = block.find('h3').text.strip()
        url = block.find('h3').find('a').get('href').strip()
        salary_tag = block.find('p', {'class': 'salary-city__vacancy'})
        salary_value = salary_tag.text.strip() if salary_tag else ''
        data.append({'title': title, 'url': url, 'salary': salary_value})
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


def parse_page(page_url):
    content = get_content(page_url)

    soup = BeautifulSoup(content, 'lxml')

    site = soup.find('dt', string="Сайт:").find_next_sibling('dd').find('a').text.strip()

    return {'url': page_url, 'site': site}


def parse_sync():
    data = []
    url = "https://job.morion.ua/jobs/"
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')
    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]

    for block in blocks:
        url = block.find('h3').find('a').get('href').strip()
        page_data = parse_page(url)
        data.append(page_data)

    with open('sync.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def parse_async():
    url = "https://job.morion.ua/jobs/"
    content = get_content(url)
    soup = BeautifulSoup(content, 'lxml')
    blocks = soup.find_all('h3')
    blocks = [block.parent for block in blocks if block.get('class') is None]
    urls = [block.find('h3').find('a').get('href').strip() for block in blocks]
    with Pool(5) as p:
        data = p.map(parse_page, urls)

    with open('async.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)



if __name__ == "__main__":
    # parse_xml()
    # parse_morin()
    # print(parse_page('https://job.morion.ua/vacancy/13894932892/'))

    # start = perf_counter()
    # parse_sync()
    # end = perf_counter()
    # print(end - start)  # 8.260

    start = perf_counter()
    parse_async()
    end = perf_counter()
    print(end - start)  # 3.4360

