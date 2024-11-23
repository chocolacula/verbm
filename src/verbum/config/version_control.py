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
        object.__setattr__(self, "major", [re.compile(r) for r in self.major])
        object.__setattr__(self, "minor", [re.compile(r) for r in self.minor])
        object.__setattr__(self, "patch", [re.compile(r) for r in self.patch])

    @staticmethod
    def default() -> Matcher:
        raw = {
            "major": [
                r"^(\* ?)?(hot)?fix ?(\(( ?\w)+\))?!: ",
                r"^(\* ?)?feat(ure)? ?(\(( ?\w)+\))?!: ",
                r"^(\* ?)?refactor(ing)? ?(\(( ?\w)+\))?!: ",
                r"(?i)^(\* ?)?BREAKING(?:\s*CHANGE)? ?(\(( ?\w)+\))?: ",
            ],
            "minor": [
                r"^(\* ?)?feat(ure)? ?(\(( ?\w)+\))?: ",
            ],
            "patch": [
                r"^(\* ?)?(hot)?fix ?(\(( ?\w)+\))?: ",
                r"^(\* ?)?refactor(ing)? ?(\(( ?\w)+\))?: ",
            ],
        }
        return Matcher(**raw)  # type: ignore


@dataclass(frozen=True)
class Commit:
    username: Optional[str] = None
    email: Optional[str] = None
    message: Optional[str] = None


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
    type: Type = Type.GIT
    matcher: Matcher = field(default_factory=Matcher.default)
    commit: Optional[Commit] = None
    tag: Optional[str] = None

    def __post_init__(self):
        if isinstance(self.type, str):
            object.__setattr__(self, "type", Type.from_str(self.type))
        object.__setattr__(self, "matcher", Matcher(**self.matcher))  # type: ignore
        object.__setattr__(self, "commit", Commit(**(self.commit or {})))  # type: ignore
