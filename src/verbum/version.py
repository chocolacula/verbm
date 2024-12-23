from __future__ import annotations
import re
from string import Template
from typing import Optional


class Version:
    """
    Version encapsulate the semantic version splitted into its components.
    """

    major: int = 0
    minor: int = 0
    patch: int = 0
    suffix: Optional[str] = None

    __format: str
    __regex: re.Pattern

    def __init__(self, format: str, version: str):
        """
        Create a new Version object with the given format which is a template string
        with $major, $minor and $patch identifiers.

        If version is provided, it will be parsed and validated against the format.
        """

        regex = Template(format).substitute(
            major="([0-9]+)", minor="([0-9]+)?", patch="([0-9]+)?", suffix="(.+)?"
        )

        self.__format = format
        self.__regex = re.compile(f"^{regex}$")

        self.parse(version)

    def __str__(self) -> str:
        return Template(self.__format).substitute(
            major=self.major,
            minor=self.minor,
            patch=self.patch,
            suffix=self.suffix or "",
        )

    def parse(self, version: str):
        # validate first
        m = re.match(self.__regex, version)
        if not m:
            raise Exception(
                f"version: '{version}' and template: '{self.__format}' don't match each other"
            )

        # keep order of keywords
        placeholders = re.findall(r"\$(\w+)", self.__format)

        if len(m.groups()) != len(placeholders):
            raise Exception(f"not enough components in: {version}")

        # guarantee order
        parsed = {}
        for i, n in enumerate(m.groups()):
            parsed[placeholders[i]] = n

        self.major = int(parsed["major"])
        if "minor" in parsed:
            self.minor = int(parsed["minor"])
        if "patch" in parsed:
            self.patch = int(parsed["patch"])
        if "suffix" in parsed:
            self.suffix = parsed["suffix"]
