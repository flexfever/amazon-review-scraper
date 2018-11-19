from lxml import html
import requests
import json, re
from dateutil import parser as dateparser
from time import sleep


class Scraper:
    AMAZON_URL = 'http://www.amazon.com/dp/'

    def __init__(self):
        pass

    def read_asins(self, asins):
        extracted_data = []
        for asin in asins:
            amazon_url = Scraper.AMAZON_URL + asin
            print("Downloading and processing page http://www.amazon.com/dp/" + asin)

            page = self.load_page(amazon_url)
            product = self.parse_product(page)
            rating = self.parse_rating(page)
            reviews = self.parse_reviews(page)

            data = {
                'product': product,
                'rating': rating,
                'reviews': reviews
            }
            extracted_data.append(data)

            sleep(5)
        f = open('data.json', 'w')
        json.dump(extracted_data, f, indent=4, ensure_ascii=False)

    def load_page(self, url):
        # Add some recent user agent to prevent amazon from blocking the request
        # Find some chrome user agent strings  here https://udger.com/resources/ua-list/browser-detail?browser=Chrome
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }

        for i in range(1):
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code == 404:
                return {"url": url, "error": "page not found"}
            if response.status_code != 200:
                continue
            page = response.text
            return page

        return {
            "error": "failed to process the page",
            "url": url
        }


    def parse_product(self, page):
        parser = html.fromstring(page)

        XPATH_PRODUCT_NAME = '//h1//span[@id="productTitle"]//text()'
        XPATH_PRODUCT_PRICE = '//span[@id="priceblock_ourprice"]/text()'

        raw_product_price = parser.xpath(XPATH_PRODUCT_PRICE)
        raw_product_name = parser.xpath(XPATH_PRODUCT_NAME)

        product_price = ''.join(raw_product_price).replace(',', '')
        product_name = ''.join(raw_product_name).strip()

        product = {}
        product.update({"name": product_name}) if product_name else product.get("name")
        product.update({"price": product_price}) if product_price else product.get("price")

        return product

    def parse_rating(self, page):
        reviews_anchor = '<a id="customerReviews" class="a-link-normal" href="#"></a>'
        html_chunks = page.split(reviews_anchor)

        html_reviews = html_chunks[1]

        parser = html.fromstring(html_reviews)

        XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
        total_ratings = parser.xpath(XPATH_AGGREGATE_RATING)

        ratings_dict = {}

        # grabing the rating  section in product page
        for ratings in total_ratings:
            extracted_rating = ratings.xpath('./td//a//text()')
            if extracted_rating:
                rating_key = extracted_rating[0]
                raw_rating_value = extracted_rating[1]
                rating_value = raw_rating_value
                if rating_key:
                    ratings_dict.update({rating_key: rating_value})

        return ratings_dict

    def parse_reviews(self, page):
        reviews_anchor = '<a id="customerReviews" class="a-link-normal" href="#"></a>'
        html_chunks = page.split(reviews_anchor)

        html_reviews = html_chunks[1]

        parser = html.fromstring(html_reviews)
        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'

        reviews = parser.xpath(XPATH_REVIEW_SECTION_1)
        if not reviews:
            reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
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
        XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
        XPATH_REVIEW_TEXT_2 = './/div//span[@data-action="columnbalancing-showfullreview"]/@data-columnbalancing-showfullreview'
        XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
        XPATH_AUTHOR = './/span[contains(@class,"profile-name")]//text()'
        XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'

        raw_review_author = review.xpath(XPATH_AUTHOR)
        raw_review_rating = review.xpath(XPATH_RATING)
        raw_review_header = review.xpath(XPATH_REVIEW_HEADER)
        raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
        raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
        raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
        raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

        # cleaning data
        author = ' '.join(' '.join(raw_review_author).split())
        review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
        review_header = ' '.join(' '.join(raw_review_header).split())

        try:
            review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
        except:
            review_posted_date = None
        review_text = ' '.join(' '.join(raw_review_text1).split())

        # grabbing hidden comments if present
        if raw_review_text2:
            json_loaded_review_data = json.loads(raw_review_text2[0])
            json_loaded_review_data_text = json_loaded_review_data['rest']
            cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
            full_review_text = review_text + cleaned_json_loaded_review_data_text
        else:
            full_review_text = review_text
        if not raw_review_text1:
            full_review_text = ' '.join(' '.join(raw_review_text3).split())

        raw_review_comments = review.xpath(XPATH_REVIEW_COMMENTS)
        review_comments = ''.join(raw_review_comments)
        review_comments = re.sub('[A-Za-z]', '', review_comments).strip()
        review_dict = {
            'review_comment_count': review_comments,
            'review_text': full_review_text,
            'review_posted_date': review_posted_date,
            'review_header': review_header,
            'review_rating': review_rating,
            'review_author': author
        }
        return review_dict