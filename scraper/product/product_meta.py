from lxml import html

from scraper.product.product_page import ProductPage

class ProductMeta:
    def __init__(self, product):
        self._product = product

        self._page = ProductPage(product)
        self._title = None

        self.initialize()

    def initialize(self):
        self._page.load()
        text = self._page.text

        XPATH_TITLE = '//span[@id="productTitle"]//text()'
        parser = html.fromstring(text)
        title = parser.xpath(XPATH_TITLE)[0].strip()
        self._title = title

    @property
    def title(self):
        return self._title
