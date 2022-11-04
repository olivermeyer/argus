from src.tasks.abstract import AbstractTask
from src.tasks.crawl_async import CrawlAsyncTask


class TaskFactory:
    mapping = {
        "crawl_async": CrawlAsyncTask,
    }

    @staticmethod
    def create(task: str, config: dict) -> AbstractTask:
        return TaskFactory.mapping[task](config)
