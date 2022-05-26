from src.tasks.abstract import AbstractTask
from src.tasks.crawl import CrawlTask
from src.tasks.crawl_async import CrawlAsyncTask


class TaskFactory:
    mapping = {
        "crawl": CrawlTask,
        "crawl_async": CrawlAsyncTask,
    }

    @staticmethod
    def create(task: str, user: str, secrets: dict) -> AbstractTask:
        return TaskFactory.mapping[task](user, secrets)
