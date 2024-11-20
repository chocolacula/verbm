from abc import ABC, abstractmethod
from typing import List, Optional


class VersionControl(ABC):
    @abstractmethod
    def add(self, *files: str):
        pass

    @abstractmethod
    def commit(self, message: str, username: Optional[str], email: Optional[str]):
        pass

    @abstractmethod
    def tag(self, tag: str):
        pass

    @abstractmethod
    def push(self, with_tags: bool):
        pass

    @abstractmethod
    def log(self, from_tag: str) -> List[str]:
        return []
