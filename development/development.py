from scraper.product.product import Product
from scraper.search.search import Search

from dotenv import load_dotenv
import json

def read_product(asin):
    product = Product(asin)

    product_meta = product.product_meta
    reviews_meta = product.reviews_meta

    product_dict = {
        'asin': product.asin,
        'title': product_meta.title,
        'review_count': reviews_meta.review_count,
        'rating': reviews_meta.rating
    }
    with open(f'{product.asin}.json', 'w', encoding='utf8') as file:
        json.dump(product_dict, file, indent=4, ensure_ascii=False)

    with open(f'{product.asin}_reviews.json', 'w', encoding='utf8') as file:
            file.write('')
    with open(f'{product.asin}_reviews.json', 'a', encoding='utf8') as file:
        file.write('[\n')
        reviews = product.get_reviews()
        for i, review in enumerate(reviews):
            json.dump(review, file, indent=4, ensure_ascii=False)
            if i < product.reviews_meta.review_count - 1:
                file.write(',\n')
            else:
                file.write('\n')
        file.write(']\n')

if __name__ == "__main__":
    load_dotenv(verbose=True)

    # search = Search('golf set')
    search_phrase = 'posture corrector for women'
    search = Search(search_phrase)
    results = search.get_results()
    results_dict = list(map(lambda r: r.as_dict(), results))

    with open(f'{search_phrase}.json', 'w', encoding='utf8') as file:
        json.dump(results_dict, file, indent=4)

    # for i, result in enumerate(results):
    #     print(i, result.asin, result.search_rank, result.sponsored)
    #     read_product(result.asin)

    # read_product('B0776MN1XL')
    read_product('B07C33N94K')


