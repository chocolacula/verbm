import re
from typing import List, Optional

from .interface import VersionControl
from .call import call


class Git(VersionControl):
    __delim = ">+>:+-\n"

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

    def log(self, from_tag: str, file_filters: List[re.Pattern]) -> List[str]:
        # useful commands:
        # call("git", "rev-list", "--max-parents=0", "HEAD")

        hash = call("git", "rev-parse", from_tag).rstrip()

        out = call(
            "git",
            "--no-pager",
            "log",
            "--decorate=short",
            f"--pretty=format:{self.__delim}%s%n%b{self.__delim}",
            "--name-only",
            f"{hash}^..HEAD",
        )
        return self.__filter(out, file_filters)

    def __filter(self, data: str, file_filters: List[re.Pattern]) -> List[str]:
        # parse data to sequence ["", commit, files, commit, files, ...]
        chunks = data.split(self.__delim)

        commits: List[str] = []

        for i in range(2, len(chunks), 2):
            fnames = chunks[i].split("\n")[1:]  # starts from ""
            matched = False

            if len(file_filters) == 0:
                matched = True
            else:
                for fname in fnames:
                    for ffilter in file_filters:
                        matched |= re.match(ffilter, fname) != None

            if matched:
                # it could be squashed and contains a few commit messages
                commit = chunks[i - 1]
                lines = list(filter(lambda s: s != "", commit.split("\n")))
                commits.extend(lines)

        return commits

    def last_tag(self) -> Optional[str]:
        try:
            return call("git", "describe", "--tags", "--abbrev=0").rstrip()
        except:
            return None

    def username(self) -> Optional[str]:
        try:
            return call("git", "config", "user.name").rstrip()
        except:
            return None

    def email(self) -> Optional[str]:
        try:
            return call("git", "config", "user.email").rstrip()
        except:
            return None
