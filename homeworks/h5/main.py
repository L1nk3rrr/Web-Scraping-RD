import re
import logging
import time
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.orm import sessionmaker, DeclarativeBase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(lineno)d -  %(message)s",
)
_logger = logging.getLogger(__name__)

SITE = "https://www.lejobadequat.com/emplois"
START_PAGE = 1
MAX_DEFAULT_PAGES_TO_PARSE = 10
MAX_THREADS = 16
LINK_TAG_PATTERN = re.compile(r"<article[^>]*>(?:.*?\n)*?.*?<a[^>]*\bhref=\"([^\"]*)\"[^>]*\btitle=\"([^\"]*)\"")
# [^\"]* - to avoid another content after title


class Base(DeclarativeBase):
    ...


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    title = Column(Text, nullable=False)


def init_db():
    engine = create_engine('sqlite:///vacancy.db')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

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
    vacancies_ = []
    for url, title in re.findall(LINK_TAG_PATTERN, text):
        vacancies_.append(Vacancy(url=url, title=title))
    return vacancies_


def fetch_page(page):
    _logger.info(f"Parsing page {page}")
    request_body = get_default_body(page)
    data = post_request(SITE, request_body)
    if data:
        return parse_info_from_text(data.get("template", ""))
    return []


def save_to_db(session_, vacancies_: list[tuple]) -> None:
    session_.bulk_save_objects(vacancies_)
    session_.commit()


def save_to_json(vacancies_: list[tuple], filename: str) -> None:
    jobs_dict = [{'id': vacancy.id, 'url': vacancy.url, 'title': vacancy.title} for vacancy in vacancies_]
    with open(filename, 'w') as f:
        json.dump(jobs_dict, f, indent=4)


def parse_lejob():
    vacancies = []
    start = time.perf_counter()
    request_body = get_default_body()

    data = post_request(SITE, request_body)
    if not data:
        _logger.info(f"First call was not successful, no data returned")

    start_page = START_PAGE + 1
    max_pages = data.get("settings", {}).get("pager", {}).get("total_pages", MAX_DEFAULT_PAGES_TO_PARSE)
    vacancies.extend(parse_info_from_text(data.get("template", "")))

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        future_to_page = {executor.submit(fetch_page, page): page for page in range(start_page, max_pages + 1)}
        for future in as_completed(future_to_page):
            vacancies.extend(future.result())

    end = time.perf_counter()
    _logger.info(f"Time performance = {end - start}")
    _logger.info(f"Found {len(vacancies)} vacancies")
    return vacancies


if __name__ == "__main__":
    session = init_db()
    result = parse_lejob()
    save_to_db(session, result)
    saved_vacancies = session.query(Vacancy).all()
    save_to_json(saved_vacancies, 'vacancy.json')
