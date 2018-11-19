from lxml import html
import json
from dateutil import parser as dateparser
import math
import time
import codecs

from scraper.request.request_service import RequestService
from scraper.request.method import *

class ReviewsParser:
    AMAZON_URL = 'http://www.amazon.com/dp/product-reviews'

    @classmethod
    def build_url(cls, asin, page):
        url = ''
        url += cls.AMAZON_URL
        url += '/' + asin
        url += '/?pageNumber=' + str(page)
        return url

    def __init__(self):
        self.request_service = RequestService()

    def process_asin(self, asin):
        url = ReviewsParser.build_url(asin, 1)
        page = self.load_page(url)

        total_review_count = self.get_total_review_count(page)
        page_count = self.get_page_count(total_review_count)

        parsed_reviews = []
        for i in range(1, page_count + 1):
            url = ReviewsParser.build_url(asin, i)
            page = self.load_page(url)
            reviews = self.parse_reviews(page)
            if reviews is not None:
                parsed_reviews.extend(reviews)
            time.sleep(0.1)

        with open('reviews.json', 'w', encoding='utf8') as file:
            json.dump(parsed_reviews, file, indent=4, ensure_ascii=False)

    def load_page(self, url):
        page = self.request_service.send_request(GET, url)
        return page

    def get_total_review_count(self, page):
        parser = html.fromstring(page)
        XPATH_TOTAL_REVIEWS = './/span[@data-hook="total-review-count"]//text()'
        raw_total_reviews = parser.xpath(XPATH_TOTAL_REVIEWS)[0]
        total_reviews = int(raw_total_reviews)
        return int(total_reviews)

    def get_page_count(self, total_review_count):
        reviews_per_page = 10
        pages = int(math.ceil(total_review_count / reviews_per_page))
        return pages

    def parse_reviews(self, page):
        parser = html.fromstring(page)
        XPATH_REVIEW = './/div[@data-hook="review"]'

        reviews = parser.xpath(XPATH_REVIEW)
        reviews_list = []

        # Parsing individual reviews
        for review in reviews:
            review_dict = self.parse_review(review)
            reviews_list.append(review_dict)

        return reviews_list

    def parse_review(self, review):
        XPATH_RATING = './/i[@data-hook="review-star-rating"]//text()'
        XPATH_REVIEW_HEADER = './/a[@data-hook="review-title"]//text()'
        XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
        XPATH_REVIEW_TEXT = './/span[@data-hook="review-body"]//text()'
        XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'

        review_id = review.attrib['id']
        raw_review_author = review.xpath(XPATH_AUTHOR)
        raw_review_rating = review.xpath(XPATH_RATING)
        raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
        raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
        raw_review_text = review.xpath(XPATH_REVIEW_TEXT)

        # cleaning data
        author = ' '.join(' '.join(raw_review_author).split())
        review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
        review_header = ' '.join(' '.join(raw_review_header).split())

        try:
            review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
        except:
            review_posted_date = None
        review_text = ' '.join(' '.join(raw_review_text).split())

        review_dict = {
            'review_id': review_id,
            'review_text': review_text,
            'review_posted_date': review_posted_date,
            'review_header': review_header,
            'review_rating': review_rating,
            'review_author': author
        }

        return review_dict
