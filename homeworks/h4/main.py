import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(lineno)d -  %(message)s",
)
_logger = logging.getLogger(__name__)

SITE = "https://www.lejobadequat.com/emplois"
START_PAGE = 1
MAX_DEFAULT_PAGES_TO_PARSE = 10
MAX_THREADS = 16
TITLE_PATTERN = re.compile(r"<div class=\"job_secteur_title\">(.*?)<\/div>")
REF_PATTERN = re.compile(r"<div class=\"job_secteur_ref\">Réf : (.*?)<\/div>")


def get_default_body(page=START_PAGE):
    # minimal amount of parameters needed in body
    return {
        "action": "facetwp_refresh",
        "data": {
            "template": "wp",
            "paged": page
        }
    }


def post_request(url: str, data: dict):
    result_data = {}
    try:
        r = requests.post(url, json=data, timeout=(5, 10))
    except Exception as e:
        _logger.info(f"Error while parsing page {data['data']['paged']}, {e}")
        return result_data

    if r.status_code == 200:
        result_data = r.json()
    _logger.info(f"Status code {r.status_code}, page {data['data']['paged']}")
    return result_data


def parse_info_from_text(text: str) -> list[str|None]:
    titles = []
    for title, ref in zip(re.findall(TITLE_PATTERN, text), re.findall(REF_PATTERN, text)):
        title_ = title.strip().replace("<wbr>", "")
        text = f"{title_} ({ref})"
        titles.append(text)
    return titles


def fetch_page(page):
    _logger.info(f"Parsing page {page}")
    request_body = get_default_body(page)
    data = post_request(SITE, request_body)
    if data:
        return parse_info_from_text(data.get("template", ""))
    return []


def parse_lejob():
    titles = []
    start = time.perf_counter()
    request_body = get_default_body()

    data = post_request(SITE, request_body)
    if not data:
        _logger.info(f"First call was not successful, no data returned")

    start_page = START_PAGE + 1
    max_pages = data.get("settings", {}).get("pager", {}).get("total_pages", MAX_DEFAULT_PAGES_TO_PARSE)
    titles = parse_info_from_text(data.get("template", ""))

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_page = {executor.submit(fetch_page, page): page for page in range(start_page, max_pages + 1)}
        for future in as_completed(future_to_page):
            titles.extend(future.result())

    end = time.perf_counter()
    _logger.info(f"Time performance = {end - start}")
    _logger.info(f"Found {len(titles)} jobs")
    if titles:
        with open("results.txt", 'w') as f:
            f.write("\n".join(titles))


if __name__ == "__main__":
    parse_lejob()
