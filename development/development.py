from scraper.product import Product

from dotenv import load_dotenv
import json


def read_product(asin):
    product = Product(asin)

    with open(f'{product.asin}.json', 'w', encoding='utf8') as file:
        file.write('')

    with open(f'{product.asin}.json', 'a', encoding='utf8') as file:
        file.write('[\n')
        count = 0
        for review in product.get_reviews():
            json.dump(review, file, indent=4, ensure_ascii=False)
            if count < product.total_review_count - 1:
                file.write(',\n')
            else:
                file.write('\n')
            count += 1
        file.write(']\n')

if __name__ == "__main__":
    load_dotenv(verbose=True)

    read_product('B0776MN1XL')
    read_product('B07C33N94K')
