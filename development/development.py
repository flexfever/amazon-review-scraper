import os

from scraper.scraper import Scraper
from scraper.reviews_parser import ReviewsParser
from scraper.request.request_service import RequestService
from scraper.request.method import *

from dotenv import load_dotenv
import os



if __name__ == "__main__":
    load_dotenv(verbose=True)

    # scraper = Scraper()
    # scraper.read_asins(['B0776MN1XL'])

    reviews_parser = ReviewsParser()
    reviews_parser.process_asin('B0776MN1XL')


    #
    # url = 'http://httpbin.org/headers'
    # # url = 'http://lumtest.com/myip.json'
    # code, response = request_service.send_request(GET, url)
    # print(code)
    # print(response)
    #
