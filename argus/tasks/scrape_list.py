from collections import defaultdict

from argus.resources.discogs import get_list_release_ids, ListingsPage
from argus.tasks.abstract import AbstractTask


class ScrapeListTask(AbstractTask):
    """
    This task is used to find the sellers with the highest number
    of listings for the releases in a list.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.list_id = self.kwargs["list_id"]
        self.sellers = self.kwargs["sellers"]

    def execute(self):
        # TODO: make this async
        release_ids = get_list_release_ids(discogs_token=self.config["discogs_token"], list_id=self.list_id)
        sellers = defaultdict(int)
        for release_id in release_ids:
            self.logger.info(f"Processing release {release_id}")
            listings_page = ListingsPage(str(release_id))
            for listing in listings_page.fetch():
                sellers[listing["seller"]] += 1
        sellers = {k: {"items": v, "url": f"https://www.discogs.com/seller/{k}/profile"} for k, v in sellers.items()}
        sorted_sellers = sorted(sellers.items(), key=lambda x: x[1]["items"], reverse=True)
        for seller in sorted_sellers[:self.sellers]:
            print(seller[0])
            print(f"  url: {seller[1]['url']}")
            print(f"  items: {seller[1]['items']}")
