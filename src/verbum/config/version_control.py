from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import re
from typing import List, Optional


@dataclass(frozen=True)
class Matcher:
    major: List[re.Pattern] = field(default_factory=list)
    minor: List[re.Pattern] = field(default_factory=list)
    patch: List[re.Pattern] = field(default_factory=list)

    def __post_init__(self):
        major = self.major
        if major == []:
            major = [
                r"^(hot)?fix ?(\(( ?\w)+\))?!: ",
                r"^feat(ure)? ?(\(( ?\w)+\))?!: ",
                r"^refactor(ing)? ?(\(( ?\w)+\))?!: ",
                r"(?i)^BREAKING(?:\s*CHANGE)? ?(\(( ?\w)+\))?: ",
            ]
        object.__setattr__(self, "major", [re.compile(r) for r in major])

        minor = self.minor
        if minor == []:
            minor = [
                r"^feat(ure)? ?(\(( ?\w)+\))?: ",
            ]
        object.__setattr__(self, "minor", [re.compile(r) for r in minor])

        patch = self.patch
        if patch == []:
            patch = [
                r"^(hot)?fix ?(\(( ?\w)+\))?: ",
                r"^refactor(ing)? ?(\(( ?\w)+\))?: ",
            ]
        object.__setattr__(self, "patch", [re.compile(r) for r in patch])


@dataclass(frozen=True)
class Git:
    username: str
    email: str
    commit_msg: str
    tag: str


class Type(Enum):
    GIT = 1
    # HG = 2
    # SVN = 3

    @staticmethod
    def from_str(s: str) -> Type:
        if s.lower() == "git":
            return Type.GIT
        else:
            raise ValueError(f"unknown type: {s}")


@dataclass(frozen=True)
class VersionControl:
    type: Optional[Type] = Type.GIT
    matcher: Optional[Matcher] = None
    git: Optional[Git] = None
    # hg: Optional[Hg] = None
    # svn: Optional[Svn] = None

    def __post_init__(self):
        if self.type:
            object.__setattr__(self, "type", Type.from_str(self.type))

        if self.matcher:
            object.__setattr__(self, "matcher", Matcher(**self.matcher))

        if self.git:
            object.__setattr__(self, "git", Git(**self.git))
