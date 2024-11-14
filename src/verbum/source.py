import os
import re
from string import Template
from typing import List

from verbum.config.config import Source
from verbum.version import Version


class SourceManager:
    """
    SourceManager is responsible for updating versions across source files.
    """

    cfg_path: str
    root: str
    sources: List[Source]

    def __init__(self, cfg_path: str, sources: List[Source]):
        self.cfg_path = cfg_path

        root = os.path.dirname(os.path.realpath(cfg_path))
        self.root = root

        self.sources = sources

    def replace(self, old_version: Version, new_version: Version):
        with open(self.cfg_path, "r+") as file:
            content = file.read()

            # space tolerant before and after the colon
            regex = f"version[ ]*:[ \n]*{old_version}$"

            m = re.match(regex, content, flags=re.MULTILINE)
            if not m:
                raise Exception("cannot match version in the config file")

            old_str = m.group(0)
            new_str = old_str.replace(str(old_version), str(new_version))

            content = content.replace(old_str, new_str)

            file.seek(0)
            file.truncate()
            file.write(content)

        for src in self.sources:
            fn = os.path.join(self.root, src.file)

            if not os.path.isfile(fn):
                raise Exception(f"cannot find: {fn}")

            old_str = Template(src.template).substitute(version=str(old_version))
            new_str = Template(src.template).substitute(version=str(new_version))

            with open(fn, "r+") as file:
                content = file.read()
                content = content.replace(old_str, new_str)

                file.seek(0)
                file.truncate()
                file.write(content)
