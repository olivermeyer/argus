from abc import ABC, abstractmethod
from logging import Logger

from src.resources.logger import logger


class AbstractTask(ABC):
    def __init__(self, config: dict, logger: Logger = logger):
        self.config = config
        self.logger = logger

    @abstractmethod
    def execute(self):
        pass
