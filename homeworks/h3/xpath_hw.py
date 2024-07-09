import requests
from lxml import html
from pathlib import Path
from itertools import chain


def parse_indeed_request():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
    }
    r = requests.get('https://br.indeed.com/', headers=headers)
    print(r.status_code)
    # unfortunately it's returning 403 and idk how to avoid this..
    # so i downloaded a file with a first, start page of the site %)

def parse_indeed_html_file():
    messages = []
    tree = html.parse('indeed.html')
    file_to_save = Path("results/xpath_results.txt")
    query = tree.xpath("//form[@id='jobsearch']//input[@name='q']")
    location = tree.xpath("//form[@id='jobsearch']//input[@name='l']")
    button = tree.xpath("//form[@id='jobsearch']//button[@type='submit']")
    for element in chain(query,location,button):
        tag = element.tag
        if tag == "input":
            text = element.attrib.get("placeholder", "")
        else:
            text = element.text
        messages.append(f"{tag} - {text}")

    file_to_save.write_text("\n".join(messages))


if __name__ == "__main__":
    # parse_indeed_request()
    parse_indeed_html_file()