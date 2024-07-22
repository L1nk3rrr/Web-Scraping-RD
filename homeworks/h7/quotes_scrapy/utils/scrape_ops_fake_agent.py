import os
import requests
from random import randint

from dotenv import load_dotenv

load_dotenv()

SCRAPEOPS_API_KEY = os.environ.get('SCRAPEOPS_API_KEY', 'YOUR API KEY')


def get_user_agent_list():
    response = requests.get('http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY)
    json_response = response.json()
    return json_response.get('result', [])


def get_random_user_agent(user_agent_list):
    random_index = randint(0, len(user_agent_list) - 1)
    return user_agent_list[random_index]
