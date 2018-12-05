class Result:
    def __init__(self, element):
        self.element = element
        self._parse()

    def _parse(self):
        attrib = self.element.attrib
        self._asin = attrib['data-asin']
        self._search_rank = attrib['data-result-rank']
        self._sponsored = self._parse_sponsored()

    def _parse_sponsored(self):
        SPONSORED_XPATH_TEMPLATE = '//div[@id="a-popover-sponsored-header-{}"]'
        SPONSORED_XPATH = SPONSORED_XPATH_TEMPLATE.format(self.asin)
        sponsored_element = self.element.xpath(SPONSORED_XPATH)

        if sponsored_element:
            return True
        else:
            return False

    @property
    def asin(self):
        return self._asin

    @property
    def search_rank(self):
        return self._search_rank

    @property
    def sponsored(self):
        return self._sponsored

    def as_dict(self):
        return {
            'asin': self.asin,
            'search_rank': self.search_rank,
            'sponsored': self.sponsored
        }