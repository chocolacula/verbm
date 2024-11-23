from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional
import os

from verbum.config.version_control import VersionControl

import yaml

DEFAULT_FILENAMES = ["version.yml", "version.yaml"]


@dataclass(frozen=True)
class Source:
    file: str
    template: str


@dataclass(frozen=True)
class Config:
    """
    Config is a root container of all configuration data, responsible for
    parsing the yaml file and storing data from it in a structured way.
    """

    path: str
    version: str
    template: str
    source: List[Source] = field(default_factory=list)
    version_control: Optional[VersionControl] = None

    def __post_init__(self):
        object.__setattr__(self, "source", [Source(**s) for s in self.source])  # type: ignore
        object.__setattr__(
            self, "version_control", VersionControl(**(self.version_control or {}))
        )

    @staticmethod
    def from_file(path: str) -> Optional[Config]:
        path = Config.__path_or_default(path)

        with open(path, "r") as f:
            data = yaml.safe_load(f)
            data["path"] = path  # required field
            c = Config(**data)
            return c

        return None

    @staticmethod
    def __path_or_default(path: str | None) -> str:
        if path is not None:
            if os.path.isfile(path):
                return path

            raise Exception(f"no such file: '{path}'")

        # else
        for fn in DEFAULT_FILENAMES:
            if os.path.isfile(fn):
                return fn

        raise Exception(f"cannot find any of: {DEFAULT_FILENAMES}")
