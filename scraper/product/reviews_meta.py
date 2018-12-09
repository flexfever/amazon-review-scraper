from scraper.product.reviews_page import ReviewsPage
from scraper.product.reviews_parser import ReviewsParser

class ReviewsMeta:
    def __init__(self, product):
        self._product = product
        self._page = ReviewsPage(product, 1)
        self._rating = None
        self._total_review_count = None
        self._page_count = None

    def initialize(self):
        self._page.load()
        text = self._page.text
        reviews_parser = ReviewsParser()
        self._rating = reviews_parser.get_rating(text)
        self._total_review_count = reviews_parser.get_total_review_count(text)
        self._page_count = reviews_parser.get_page_count(self._total_review_count)

        print(f"Total reviews: {self.review_count}")
        print(f"Pages of reviews: {self.page_count}")

    @property
    def review_count(self):
        return self._total_review_count

    @property
    def rating(self):
        return self._rating

    @property
    def page_count(self):
        return self._page_count
