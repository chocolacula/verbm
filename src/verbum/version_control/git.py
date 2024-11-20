from typing import List, Optional

from verbum.version_control.interface import VersionControl
from verbum.version_control.call import call


class Git(VersionControl):
    def add(self, *files: str):
        call("git", "add", *files)

    def commit(self, message: str, username: Optional[str], email: Optional[str]):
        committer = []
        if username:
            committer.extend(["-c", f'user.name="{username}"'])
        if email:
            committer.extend(["-c", f'user.email="{email}"'])

        call("git", *committer, "commit", "-m", message)

    def tag(self, tag: str):
        call("git", "tag", tag)

    def push(self, with_tags: bool):
        call("git", "push")

        if with_tags:
            call("git", "push", "--tags")

    def log(self, from_tag: str) -> List[str]:
        return []
