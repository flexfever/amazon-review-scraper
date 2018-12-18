from scraper.product.product import Product
from scraper.search.search import Search
from scraper.core.utils import to_serializable

from dotenv import load_dotenv
import json
import os

def read_product(directory, asin):
    product = Product(asin)
    product.load()

    product_meta = product.product_meta
    reviews_meta = product.reviews_meta

    product_dict = {
        'asin': product.asin,
        'title': product_meta.title,
        'brand': product_meta.brand,
        'bsr': product_meta.best_sellers_rank,
        'category': product_meta.category,
        'review_count': reviews_meta.review_count,
        'rating': reviews_meta.rating,
    }
    with open(f'{directory}/{product.asin}.json', 'w', encoding='utf8') as file:
        json.dump(product_dict, file, indent=4, ensure_ascii=False)

    # with open(f'{directory}/{product.asin}_reviews.json', 'w', encoding='utf8') as file:
    #         file.write('')
    # with open(f'{directory}/{product.asin}_reviews.json', 'a', encoding='utf8') as file:
    #     file.write('[\n')
    #     reviews = product.get_reviews()
    #     for i, review in enumerate(reviews):
    #         json.dump(review, file, indent=4, ensure_ascii=False)
    #         if i < product.reviews_meta.review_count - 1:
    #             file.write(',\n')
    #         else:
    #             file.write('\n')
    #     file.write(']\n')

if __name__ == "__main__":
    load_dotenv(verbose=True)

    search_phrase = 'posture corrector for women'
    search = Search(search_phrase)
    search.load()

    meta = search.search_meta
    results = search.get_results()
    search_dict = {
        'meta': meta,
        'results': results
    }

    directory = search_phrase.replace(" ", "_")
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(f'{directory}/search.json', 'w', encoding='utf8') as file:
        json.dump(search_dict, file, default=to_serializable, indent=4)

    # for i, result in enumerate(results):
    #     print(i, result.asin, result.search_rank, result.sponsored)
    #     read_product(directory, result.asin)
    #
    # read_product('B0776MN1XL')
    read_product(directory, 'B07C33N94K')


