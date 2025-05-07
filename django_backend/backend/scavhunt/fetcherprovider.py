import scavhunt.fetcher as fetcher
import scavhunt.fakefetcher as ff

class FetcherProvider():

    def __init__(self, is_prod: bool):
        self.is_prod = is_prod

    def get_fetcher(self) -> fetcher.Fetcher:
        return ff.FakeFetcher()