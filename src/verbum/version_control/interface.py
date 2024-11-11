from abc import ABC, abstractmethod
from typing import List


class VersionControl(ABC):

    @abstractmethod
    def commit(self, message: str):
        pass

    @abstractmethod
    def tag(self, tag: str):
        pass

    @abstractmethod
    def push(self, with_tags: bool):
        pass

    @abstractmethod
    def log(self, from_tag: str) -> List[str]:
        pass
