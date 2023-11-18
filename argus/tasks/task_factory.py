from argus.tasks.abstract import AbstractTask
from argus.tasks.find_non_master_releases_in_list import CleanListsTask
from argus.tasks.find_new_listings import FindNewListingsTask
from argus.tasks.scrape_list import ScrapeListTask


class TaskFactory:
    mapping = {
        "crawl_wantlist": FindNewListingsTask,
        "scrape_list": ScrapeListTask,
        "clean_lists": CleanListsTask,
    }

    @staticmethod
    def create(task: str, **kwargs) -> AbstractTask:
        return TaskFactory.mapping[task](**kwargs)
