import json
from time import perf_counter

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


def timeit(func):
    def wrapper_func():
        start_time = perf_counter()
        func()
        end_time = perf_counter()
        print(f'Elapsed time: {end_time - start_time}')
    return wrapper_func

@timeit
def parse_job_aon_selenium():
    driver = webdriver.Chrome()

    max_page = 11
    result = []

    for page in range(1, max_page):
        driver.get(f"https://jobs.aon.com/jobs?page={page}")

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "job-title-link")))

        # content = driver.page_source
        # soup = Beat...

        jobs = driver.find_elements(By.CLASS_NAME, "job-title-link")
        for job in jobs:
            link = job.get_attribute('href')
            title = job.find_element(By.TAG_NAME, 'span').text
            result.append({
                'title': title,
                'link': link
            })

    driver.close()
    with open('jobs_selenium.json', 'w') as f:
        json.dump(result, f, indent=4)


def pasrse_job_aon_from():
    driver = webdriver.Chrome()
    driver.get(f"https://jobs.aon.com/jobs?page=1")
    driver.implicitly_wait(1)
    before = driver.find_element(By.ID, 'search-results-indicator').text
    print('Count before:', before)

    input_search_element = driver.find_element(By.ID, 'keyword-search')
    input_search_element.send_keys('Engineer')

    button = driver.find_element(By.ID, 'search-btn')
    button.click()

    after = driver.find_element(By.ID, 'search-results-indicator').text

    print('Count after:', after)

    driver.close()

@timeit
def parse_job_aon_common():
    max_page = 11
    result = []
    for page in range(1, max_page):
        response = requests.get(
            f"https://jobs.aon.com/api/jobs?page={page}&sortBy=relevance&descending=false&internal=false",
                headers={
                    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"
        })
        data = response.json()['jobs']
        for job in data:
            title = job['data']['title']
            link = f"https://jobs.aon.com/jobs/{job['data']['slug']}"
            result.append({
                'title': title,
                'link': link
            })

    with open('jobs_common.json', 'w') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    parse_job_aon_selenium()
    # pasrse_job_aon_from()
    parse_job_aon_common()