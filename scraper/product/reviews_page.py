from scraper.core.page import Page
from scraper.product.reviews_parser import ReviewsParser

class ReviewsPage(Page):
    BASE_URL = 'http://www.amazon.com/dp/product-reviews'

    @classmethod
    def build_root_url(cls, asin):
        url = ''
        url += cls.BASE_URL
        url += '/' + asin
        return url

    def __init__(self, product, page_number):
        url = ReviewsPage.build_root_url(product.asin)
        params = {
            'pageNumber': page_number
        }
        super().__init__(url, params)

        self.product = product
        self.reviews_parser = ReviewsParser()
        self.page_number = page_number

    def get_reviews(self):
        if self.text is None:
            return None

        reviews = self.reviews_parser.parse_reviews(self.text)
        return reviews