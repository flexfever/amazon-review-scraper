from abc import ABCMeta
import time

from scraper.request.request_service import RequestService
from scraper.request.method import *

class Page(metaclass=ABCMeta):
    def __init__(self, url, params = None):
        self._request_service = RequestService()
        self._url = url
        self._params = params
        self._text = None

    @property
    def url(self):
        return self._url

    @property
    def params(self):
        return self._params

    @property
    def text(self):
        return self._text

    def load(self):
        retries = 5
        for i in range(retries):
            try:
                print(f'Loading {self.url}')
                text = self._request_service.send_request(GET, self.url, self.params)
                self._text = text
                return
            except RequestService.RequestException as e:
                print(e)
                print(f'Retrying in {i + 1} seconds.')
                time.sleep(i + 1)
        print(f'Unable to load page {self.url}')
