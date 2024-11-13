from __future__ import annotations
import re
from string import Template


class Version:
    """
    Version encapsulate the semantic version splitted into its components.
    """

    major: int
    minor: int
    patch: int

    __format: str
    __regex: re.Pattern

    def __init__(self, format: str, version: str = ""):
        """
        Create a new Version object with the given format which is a template string
        with $major, $minor and $patch identifiers.

        If version is provided, it will be parsed and validated against the format.
        """
        # self.template = template

        regex = Template(format).substitute(
            major="[0-9]+", minor="[0-9]+", patch="[0-9]+"
        )
        self.__format = format
        self.__regex = re.compile(f"^{regex}$")

        if version:
            self.parse(version)

    def parse(self, version: str):
        # validate first
        self.validate(version)

        ph = re.findall(r"\$(\w+)", self.__format)
        numbers = re.findall(r"[0-9]+", version)

        if len(numbers) < len(ph):
            raise Exception(f"not enough components in: {version}")

        # guarantee order
        parsed = {}
        for i, n in enumerate(numbers):
            parsed[ph[i]] = int(n)

        self.major = parsed["major"]
        self.minor = parsed["minor"]
        self.patch = parsed["patch"]

    def validate(self, version):
        m = re.match(self.__regex, version)
        if m == None:
            raise Exception(
                f"version: '{version}' and template: '{self.__format}' don't match each other"
            )

    def __str__(self) -> str:
        return Template(self.__format).substitute(
            major=self.major, minor=self.minor, patch=self.patch
        )
