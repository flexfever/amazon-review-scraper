from fake_useragent import UserAgent
import requests
import os

from scraper.request.method import Method

class RequestService:
    def __init__(self):
        self.user_agent_generator = UserAgent()

    def build_headers(self):
        headers = {
            'Connection': 'close',
            'accept-encoding': 'gzip, deflate',
            'User-Agent': self.user_agent_generator.random
        }
        return headers

    def get_proxies(self):
        username = os.getenv("PROXY_AUTH_USERNAME")
        password = os.getenv("PROXY_AUTH_PASSWORD")
        proxy_url = os.getenv("PROXY_URL")
        proxy_port = os.getenv("PROXY_PORT")
        proxies = {
            'http': f'http://{username}:{password}@{proxy_url}:{proxy_port}'
        }
        return proxies

    def send_request(self, method, url):
        session = requests.Session()
        session.headers = self.build_headers()
        session.proxies = self.get_proxies()

        for i in range(1):
            if method == Method.GET:
                response = session.get(url, verify=False)
            else:
                return None

            code = response.status_code
            if code == 200:
                return response.text

        return None
