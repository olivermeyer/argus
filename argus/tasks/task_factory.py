from argus.tasks.abstract import AbstractTask
from argus.tasks.crawl_async import CrawlAsyncTask
from argus.tasks.scrape_list import ScrapeListTask


class TaskFactory:
    mapping = {
        "crawl_async": CrawlAsyncTask,
        "scrape_list": ScrapeListTask,
    }

    @staticmethod
    def create(task: str, **kwargs) -> AbstractTask:
        return TaskFactory.mapping[task](**kwargs)
