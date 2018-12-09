from lxml import html
import re

from scraper.search.search_page import SearchPage
from scraper.search.search_meta import SearchMeta
from scraper.search.result import Result

class Search:
    def __init__(self, search_string):
        self.search_string = search_string
        self._page = SearchPage(self)
        self._search_meta = SearchMeta(self)

    def load(self):
        self._search_meta.initialize()
        self._page.load()

    def get_results(self):
        results = self._parse_results()
        return results

    @property
    def page(self):
        return self._page

    @property
    def search_meta(self):
        return self._search_meta

    def _parse_results(self):
        page_text = self.page.text
        parser = html.fromstring(page_text)

        result_regex = r'id="result_\d+"'
        results = re.findall(result_regex, page_text)
        results = list(set(results))
        result_count = len(results)

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
