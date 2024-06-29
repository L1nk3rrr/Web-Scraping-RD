import re
import time

import requests


def use_get():
    response = requests.get('https://www.lejobadequat.com/emplois')
    print(f'{response.status_code=}')
    print(response.text)


def use_post():
    payload = {
        "action": "facetwp_refresh",
        "data": {
        "facets": {
          "recherche": [],
          "ou": [],
          "type_de_contrat": [],
          "fonction": [],
          "load_more": [
            2
          ]
        },
        "frozen_facets": {
          "ou": "hard"
        },
        "http_params": {
          "get": [],
          "uri": "emplois",
          "url_vars": []
        },
        "template": "wp",
        "extras": {
          "counts": True,
          "sort": "default"
        },
        "soft_refresh": 1,
        "is_bfcache": 1,
        "first_load": 0,
        "paged": 1
        }
        }
    response = requests.post('https://www.lejobadequat.com/emplois', json=payload)
    print(f'{response.status_code=}')
    print(response.json()['template'])


def use_header():
    pattern = r'<th>USER-AGENT<\/th>\s*<td><span class="code detected_result">(.*)<\/span><\/td>'
    response = requests.get('https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/')
    user_agent = re.search(pattern, response.text).group(1)
    print(user_agent)
    time.sleep(1)
    response = requests.get('https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending/',
                            headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"})
    user_agent = re.search(pattern, response.text).group(1)
    print(user_agent)


def use_proxy():
    pattern = r'div.*id=[\'\"]d_clip_button[\'\"]>\s+<span>(.*)<\/span>'
    response = requests.get('https://2ip.io/')
    local_ip_address = re.search(pattern, response.text).group(1)
    print(local_ip_address)
    proxy = '111.111.111.11'
    port = 10202
    proxies = {
        'http': f'http://{proxy}:(port)',
        'https': f'http://{proxy}:{port}'
    }
    response = requests.get('https://2ip.io/', proxies=proxies, timeout=10)
    print(response.text)


if __name__ == "__main__":
    # use_get()
    # use_post()
    # use_header()
    use_proxy()