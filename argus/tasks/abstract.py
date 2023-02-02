from abc import ABC, abstractmethod
from logging import Logger

from argus.resources.logger import logger


class AbstractTask(ABC):
    def __init__(self, config: dict, logger: Logger = logger, **kwargs):
        self.config = config
        self.logger = logger
        self.kwargs = kwargs

    @abstractmethod
    def execute(self):
        pass
