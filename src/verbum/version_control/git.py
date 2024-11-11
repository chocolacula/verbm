from typing import List

from verbum.version_control.interface import VersionControl
from verbum.version_control.call import call


class Git(VersionControl):
    def commit(self, message: str):
        call("git", "commit", "-m", message)

    def tag(self, tag: str):
        call("git", "tag", tag)

    def push(self, with_tags: bool):
        call("git", "push")

        if with_tags:
            call("git", "push", "--tags")

    def log(self, from_tag: str) -> List[str]:
        return []
