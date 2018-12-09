from lxml import html

import re

from scraper.product.product_page import ProductPage

class ProductMeta:
    XPATH_TITLE = '//span[@id="productTitle"]//text()'
    XPATH_BRAND = '//a[@id="bylineInfo"]//text()'
    XPATH_BEST_SELLERS_RANK = '//li[@id="SalesRank"]'

    def __init__(self, product):
        self._product = product

        self._title = None
        self._brand = None
        self._best_sellers_rank = None
        self._category = None

    def initialize(self):
        page = ProductPage(self._product)
        page.load()
        text = page.text
        parser = html.fromstring(text)

        self._parse_title(parser)
        self._parse_brand(parser)
        self._parse_best_sellers_rank(parser)

    def _parse_title(self, parser):
        title_elements = parser.xpath(ProductMeta.XPATH_TITLE)
        if len(title_elements) > 0:
            title = title_elements[0].strip()
            self._title = title
        else:
            self._title = f"Unknown title for ASIN {self._product.asin}"

    def _parse_brand(self, parser):
        brand_elements = parser.xpath(ProductMeta.XPATH_BRAND)
        if len(brand_elements) > 0:
            brand = brand_elements[0].strip()
            self._brand = brand
        else:
            self._brand = f"Unknown brand for ASIN {self._product.asin}"

    def _parse_best_sellers_rank(self, parser):
        raw_best_sellers_rank = parser.xpath(ProductMeta.XPATH_BEST_SELLERS_RANK)

        if len(raw_best_sellers_rank) == 0:
            self._best_sellers_rank = -1
            self._category = 'Unknown'
            return

        raw_best_sellers_rank = raw_best_sellers_rank[0].text_content()
        raw_best_sellers_rank = raw_best_sellers_rank.strip()
        raw_best_sellers_rank = raw_best_sellers_rank.replace(',', '')

        best_sellers_rank_regex = r'#(\d*)'
        best_sellers_rank = re.search(best_sellers_rank_regex, raw_best_sellers_rank).group(1)
        self._best_sellers_rank = int(best_sellers_rank)

        category_regex = r'in (.*) \('
        category = re.search(category_regex, raw_best_sellers_rank).group(1)
        self._category = category

    @property
    def title(self):
        return self._title

    @property
    def brand(self):
        return self._brand

    @property
    def best_sellers_rank(self):
        return self._best_sellers_rank

    @property
    def category(self):
        return self._category
