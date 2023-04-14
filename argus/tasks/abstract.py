from abc import ABC, abstractmethod
from logging import Logger
import discogs_client

from argus.resources.logger import logger


class AbstractTask(ABC):
    def __init__(self, config: dict, logger: Logger = logger, **kwargs):
        self.config = config
        self.logger = logger
        self.kwargs = kwargs
        self.discogs_client = discogs_client.Client(
            user_agent="Argus",
            user_token=self.config["discogs_token"],
        )

    @abstractmethod
    def execute(self):
        pass
