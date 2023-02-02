from argus.tasks.abstract import AbstractTask
from argus.tasks.crawl_wantlist import CrawlWantlistTask
from argus.tasks.scrape_list import ScrapeListTask


class TaskFactory:
    mapping = {
        "crawl_wantlist": CrawlWantlistTask,
        "scrape_list": ScrapeListTask,
    }

    @staticmethod
    def create(task: str, **kwargs) -> AbstractTask:
        return TaskFactory.mapping[task](**kwargs)
