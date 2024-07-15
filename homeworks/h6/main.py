import requests
import json
from dataclasses import dataclass, asdict

from bs4 import BeautifulSoup, Tag

MAIN_URL = "https://www.bbc.com"
SPORT_URL = "https://www.bbc.com/sport"


@dataclass
class ArticleData:
    link: str
    topics: list


def fetch_and_parse(url: str) -> BeautifulSoup:
    response = requests.get(
        url=url,
        headers={
            "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        }
    )
    return BeautifulSoup(response.text, "lxml")


def extract_article_data(div: Tag) -> ArticleData:
    link = div.find('a').attrs.get('href')
    if link:
        full_link = MAIN_URL + link
        link_content = fetch_and_parse(full_link)
        related_topics = link_content.find('div', {'data-component': 'topic-list'}).find_all('li')
        topics = [topic.text.strip() for topic in related_topics if topic.text.strip()]
        return ArticleData(link=full_link, topics=topics)
    return None


def parse_bbc() -> list[ArticleData]:
    parsed_articles = []
    soup = fetch_and_parse(SPORT_URL)
    divs = soup.find_all('div', {'data-testid': 'promo', 'type': 'article'}, limit=5)

    for div in divs:
        article_data = extract_article_data(div)
        if article_data:
            parsed_articles.append(article_data)
    return parsed_articles


def save_data_to_json(data: list[ArticleData], filename: str = 'result.json') -> None:
    data_dict = [asdict(article) for article in data]
    with open(filename, 'w') as f:
        json.dump(data_dict, f, indent=4)


if __name__ == '__main__':
    result = parse_bbc()
    save_data_to_json(result)
