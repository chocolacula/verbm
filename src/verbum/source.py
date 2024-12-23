import os
import re
from string import Template
from typing import List

from .config.config import Source
from .version import Version


class SourceManager:
    """
    SourceManager is responsible for updating versions across source files.
    It keeps track of the absolute path to each file, including the configuration file, and can return these paths when needed.
    """

    cfg_path: str
    root: str
    sources: List[Source]

    def __init__(self, cfg_path: str, sources: List[Source]):
        self.cfg_path = os.path.realpath(cfg_path)

        root = os.path.dirname(self.cfg_path)
        self.root = root

        self.sources = sources
        for s in self.sources:
            s.file = os.path.realpath(os.path.join(self.root, s.file))

    def consistent(self, version: Version) -> bool:
        if not self.__contains(self.cfg_path, version):
            return False

        for src in self.sources:
            if not self.__contains(src.file, version):
                return False

        return True

    def __contains(self, path: str, version: Version) -> bool:
        """
        Checks the file with corresponding path contains specified version
        """
        if not os.path.isfile(path):
            raise Exception(f"cannot find: {path}")

        with open(path, "r+") as file:
            if file.read().find(str(version)) < 1:
                print(f"file: {path} doesn't contain version: {version}")
                return False

        return True

    def replace(self, old_version: Version, new_version: Version):
        with open(self.cfg_path, "r+") as file:
            content = file.read()

            # space tolerant before and after the colon
            regex = re.compile(f"version *:[ \n]*{re.escape(str(old_version))}")

            m = re.search(regex, content)
            if not m:
                raise Exception("cannot match version in the config file")

            old_str = m.group(0)
            new_str = old_str.replace(str(old_version), str(new_version))

            content = content.replace(old_str, new_str)

            file.seek(0)
            file.truncate()
            file.write(content)

        for src in self.sources:
            if not os.path.isfile(src.file):
                raise Exception(f"cannot find: {src.file}")

            old_str = Template(src.template).substitute(version=str(old_version))
            new_str = Template(src.template).substitute(version=str(new_version))

            with open(src.file, "r+") as file:
                content = file.read()
                content = content.replace(old_str, new_str)

                file.seek(0)
                file.truncate()
                file.write(content)

    def files(self) -> List[str]:
        return [self.cfg_path] + list(map(lambda x: x.file, self.sources))
