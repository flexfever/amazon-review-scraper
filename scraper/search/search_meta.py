from datetime import datetime

from scraper.utils import to_serializable

class SearchMeta:
    def __init__(self, search):
        self._search = search
        self._time = None

    def initialize(self):
        self._time = datetime.now()

    @property
    def time(self):
        return self._time

    def as_dict(self):
        return {
            'time': self.time
        }

@to_serializable.register(SearchMeta)
def ts_search_meta(val):
    return val.as_dict()