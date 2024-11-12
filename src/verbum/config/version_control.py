from dataclasses import dataclass
from enum import Enum
import re
from typing import List


@dataclass
class Matcher:
    major: List[re.Pattern]
    minor: List[re.Pattern]
    patch: List[re.Pattern]

    # def __init__(self, data):
    #     if "major" in data:
    #         self.major = [re.compile(r) for r in data["major"]]
    #     else:
    #         self.major = [
    #             r"^(hot)?fix ?(\(( ?\w)+\))?!: ",
    #             r"^feat(ure)? ?(\(( ?\w)+\))?!: ",
    #             r"^refactor(ing)? ?(\(( ?\w)+\))?!: ",
    #             r"(?i)^BREAKING(?:\s*CHANGE)? ?(\(( ?\w)+\))?: ",
    #         ]

    #     if "minor" in data:
    #         self.minor = [re.compile(r) for r in data["minor"]]
    #     else:
    #         self.minor = [r"^feat(ure)? ?(\(( ?\w)+\))?: "]

    #     if "patch" in data:
    #         self.patch = [re.compile(r) for r in data["patch"]]
    #     else:
    #         self.patch = [
    #             r"^(hot)?fix ?(\(( ?\w)+\))?: ",
    #             r"^refactor(ing)? ?(\(( ?\w)+\))?: ",
    #         ]


@dataclass
class Git:
    username: str
    email: str
    commit_msg: str
    tag: str


class Type(Enum):
    GIT = "git"
    # HG = "hg"
    # SVN = "svn"


@dataclass
class VersionControl:
    type: Type
    matcher: Matcher
    git: Git
    # hg: Hg
    # svn: Svn
