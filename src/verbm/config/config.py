from __future__ import annotations

from typing import List
import os

from pydantic import BaseModel
import yaml

from .version_control import VersionControl


DEFAULT_FILENAMES = ["version.yml", "version.yaml"]


class Source(BaseModel):
    file: str
    template: str


class Config(BaseModel):
    """
    Config is a root container of all configuration data, responsible for
    parsing the yaml file and storing data from it in a structured way.
    """

    path: str
    version: str
    template: str
    source: List[Source] = []
    version_control: VersionControl = VersionControl()

    @staticmethod
    def from_file(path: str | None) -> Config:
        path = Config._path_or_default(path)

        with open(path, "r") as f:
            data = yaml.safe_load(f)
            data["path"] = path  # required field
            c = Config(**data)
            return c

    @staticmethod
    def _path_or_default(path: str | None) -> str:
        if path is not None:
            if os.path.isfile(path):
                return path

            raise Exception(f"no such file: '{path}'")

        # else
        for fn in DEFAULT_FILENAMES:
            if os.path.isfile(fn):
                return fn

        raise Exception(f"cannot find any of: {DEFAULT_FILENAMES}")
