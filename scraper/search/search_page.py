from scraper.page import Page

class SearchPage(Page):
    BASE_URL = 'https://www.amazon.com/s/ref=nb_sb_ss'

    KEYWORDS_KEY = 'field-keywords'

    def __init__(self, search):
        url = SearchPage.BASE_URL
        params = {
            'url': 'search-alias=aps',
            SearchPage.KEYWORDS_KEY: search.search_string
        }
        super().__init__(url, params)
