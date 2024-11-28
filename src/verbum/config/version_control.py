from __future__ import annotations
from enum import Enum
import re
from typing import List, Optional

from pydantic import BaseModel


class Matcher(BaseModel):
    major: List[re.Pattern] = []
    minor: List[re.Pattern] = []
    patch: List[re.Pattern] = []

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


class Commit(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    message: str = "Version bumped from $version to $new_version"


class Type(str, Enum):
    GIT = "git"
    HG = "hg"
    SVN = "svn"


class VersionControl(BaseModel):
    type: Type = Type.GIT
    matcher: Matcher = Matcher.default()
    commit: Commit = Commit()
    tag: str = "v$new_version"
