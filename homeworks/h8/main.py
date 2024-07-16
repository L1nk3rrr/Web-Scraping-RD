import json

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

MAX_PAGE = 2
JOBS_LIST_XPATH = ".//div[@class='ais-Hits']/ol"
JOB_ITEM_XPATH = f"{JOBS_LIST_XPATH}/li"


def parse_page(driver, url: str, page: int):
    jobs_list = []
    driver.get(f"{url}?page={page}")
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, JOBS_LIST_XPATH)))
    jobs = driver.find_elements(By.XPATH, JOB_ITEM_XPATH)
    for job in jobs:
        title = job.find_element(By.TAG_NAME, 'h3').text  # only one h3 tag exist inside item body
        url = job.find_element(By.TAG_NAME, 'a').get_attribute('href')  # only one a tag exist inside item body
        jobs_list.append({
            'title': title,
            'url': url
        })
    return jobs_list


def save_jobs_data(jobs_list, dest_path: str = 'jobs_selenium.json') -> None:
    with open(dest_path, 'w') as f:
        json.dump(jobs_list, f, indent=4)


def parse_markandspenser():
    result = []
    url = "https://jobs.marksandspencer.com/job-search"
    driver = webdriver.Chrome()

    for page in range(1, MAX_PAGE + 1):
        jobs_from_page = parse_page(driver, url, page)
        result.extend(jobs_from_page)

    driver.close()
    return result


if __name__ == '__main__':
    jobs_data = parse_markandspenser()
    save_jobs_data(jobs_data)
