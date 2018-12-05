from scraper.page import Page

class ProductPage(Page):
    BASE_URL = 'http://www.amazon.com/dp'

    @classmethod
    def build_root_url(cls, asin):
        url = ''
        url += cls.BASE_URL
        url += '/' + asin
        return url

    def __init__(self, product):
        url = ProductPage.build_root_url(product.asin)
        super().__init__(url)

        self._product = product
