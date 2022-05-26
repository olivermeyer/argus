from abc import ABC, abstractmethod
from logging import Logger

from src.resources.logger import logger


class AbstractTask(ABC):
    def __init__(self, user, secrets, logger: Logger = logger):
        self.user = user
        self.secrets = secrets
        self.logger = logger

    @abstractmethod
    def execute(self):
        pass
