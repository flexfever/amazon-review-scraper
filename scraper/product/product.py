from scraper.product.product_meta import ProductMeta
from scraper.product.reviews_meta import ReviewsMeta
from scraper.product.reviews_page import ReviewsPage

import time

class Product:
    def __init__(self, asin):
        self.asin = asin
        self._product_meta = ProductMeta(self)
        self._reviews_meta = ReviewsMeta(self)

    @property
    def product_meta(self):
        return self._product_meta

    @property
    def reviews_meta(self):
        return self._reviews_meta

    def _get_reviews_page(self, page_number):
        return ReviewsPage(self, page_number)

    def get_reviews(self):
        for i in range(self.reviews_meta.page_count):
            page = self._get_reviews_page(i + 1)
            page.load()
            reviews = page.get_reviews()
            if reviews is None:
                continue
            for review in reviews:
                yield review

            # Delay between page loading
            time.sleep(0.1)
