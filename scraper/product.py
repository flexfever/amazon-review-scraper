from scraper.reviews_parser import ReviewsParser

from scraper.request.request_service import RequestService
from scraper.request.method import *

import time
import math

class ReviewsPage:
    PAGE_SUFFIX = '/?pageNumber='

    def __init__(self, product, page_number):
        self.request_service = RequestService()
        self.reviews_parser = ReviewsParser()

        self.product = product
        self.page_number = page_number

        root = product.reviews_root_url
        self.url = root + ReviewsPage.PAGE_SUFFIX + str(page_number)
        self.text = None

    def load(self):
        retries = 5
        for i in range(retries):
            try:
                print(f'Loading {self.url}')
                page = self.request_service.send_request(GET, self.url)
                self.text = page
                return
            except RequestService.RequestException as e:
                print(e)
                print(f'Retrying in {i} seconds.')
                time.sleep(i + 1)
        print(f'Unable to load page {self.url}')

    def get_reviews(self):
        if self.text is None: return None

        reviews = self.reviews_parser.parse_reviews(self.text)
        return reviews


class Product:
    REVIEWS_BASE_URL = 'http://www.amazon.com/dp/product-reviews'

    @classmethod
    def build_root_url(cls, asin):
        url = ''
        url += cls.REVIEWS_BASE_URL
        url += '/' + asin
        return url

    def __init__(self, asin):
        self.reviews_parser = ReviewsParser()

        self.asin = asin

        self.reviews_root_url = Product.build_root_url(asin)
        self.total_review_count = None
        self.page_count = None

        self.initialize()
        print(f"Total reviews: {self.total_review_count}")
        print(f"Pages of reviews: {self.page_count}")

    def initialize(self):
        page = self.get_reviews_page(0)
        page.load()
        text = page.text
        self.total_review_count = self.reviews_parser.get_total_review_count(text)
        self.page_count = self.reviews_parser.get_page_count(self.total_review_count)

    def get_reviews_page(self, page_number):
        return ReviewsPage(self, page_number)

    def get_reviews_page_from_review_number(self, review_number):
        reviews_per_page = 10
        page_number = int(math.floor(review_number / reviews_per_page))
        reviews_page = self.get_reviews_page(page_number)
        return reviews_page

    def get_reviews(self):
        for i in range(self.page_count):
            page = self.get_reviews_page(i + 1)
            page.load()
            reviews = page.get_reviews()
            if reviews is None:
                continue
            for review in reviews:
                yield review

            # Delay between page loading
            time.sleep(0.1)
