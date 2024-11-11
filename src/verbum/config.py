import os
from typing import List
import yaml

DEFAULT_FILENAMES = ["version.yml", "version.yaml"]


class Source:
    file: str
    template: str

    def __init__(self, file, template):
        self.file = file
        self.template = template


class Config:
    path: str
    version: str
    template: str
    source: List[Source]

    def __init__(self, path):
        path = Config.__path_or_default(path)
        self.path = path

        with open(self.path, "r") as f:
            data = yaml.safe_load(f)
            self.__dict__.update(data)

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
