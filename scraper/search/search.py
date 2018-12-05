from lxml import html
import re

from scraper.request.request_service import RequestService
from scraper.request.method import *
from scraper.search.result import Result

class Search:
    SEARCH_BASE_URL = 'https://www.amazon.com/s/ref=nb_sb_ss'

    KEYWORDS_KEY = 'field-keywords'

    def __init__(self, search_string):
        self.request_service = RequestService()
        self.search_string = search_string

    def get_results(self):
        page_text = self.execute()
        results = self.parse_results(page_text)
        return results

    def parse_results(self, page_text):
        parser = html.fromstring(page_text)

        result_regex = r'id="result_\d+"'
        results = re.findall(result_regex, page_text)
        results = list(set(results))
        result_count = len(results)

        print(result_count)

        XPATH_PRODUCT_TEMPLATE = '//li[@id="result_{}"]'

        unique_asins = []
        unique_product_elements = []
        r = range(0, result_count)
        for i in r:
            xpath_product = XPATH_PRODUCT_TEMPLATE.format(i)
            product_elements = parser.xpath(xpath_product)
            if len(product_elements) == 0:
                continue
            product_element = product_elements[0]
            if 'data-asin' in product_element.attrib:
                asin = product_element.attrib['data-asin']
                if asin not in unique_asins:
                    unique_asins.append(asin)
                    unique_product_elements.append(product_element)

        products = []
        for product_element in unique_product_elements:
            product = Result(product_element)
            products.append(product)

        return products

    def execute(self):
        search_string = self.search_string
        payload = {
            'url': 'search-alias=aps',
            Search.KEYWORDS_KEY: search_string
        }
        response = self.request_service.send_request(GET, Search.SEARCH_BASE_URL, payload)

        with open(f'{search_string}.html', 'a', encoding='utf8') as file:
            file.write(response)

        return response


