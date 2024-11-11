import sys
import os
import subprocess
import json
import argparse
import enum

from sys import stderr
from sys import stdout

from typing import Optional
from typing import Tuple

from verbum.clap import parser

VERSION = "0.0.1"

"""
def parse_version(string) -> Optional[Tuple[int, int, int]]:
    chunks = string.split(".")

    if len(chunks) != 3:
        stderr.write(f"version {string} is invalid\n")
        return None

    try:
        major = int(chunks[0])
        minor = int(chunks[1])
        patch = int(chunks[2])
    except ValueError:
        stderr.write(f"version {string} is invalid\n")
        return None

    if major < 0 or minor < 0 or patch < 0:
        stderr.write(f"version {string} is invalid\n")
        return None

    return (major, minor, patch)


class Context:
    def __init__(self, filepath):
        if filepath == None:
            filepath = os.path.dirname(os.path.realpath(__file__))
            filepath = os.path.join(filepath, DFILE)

        if os.path.exists(filepath):
            self.file = open(filepath, "r+")
            self.data = json.load(self.file)
        else:
            self.data = {}
            stderr.write("Manifest file doesn't exist\n")

    def write_version(self, version: str):
        self.data["version"] = version

        self.file.seek(0)
        self.file.truncate()
        json.dump(self.data, self.file, indent=INDENT)
        self.file.write("\n")  # trailing line
        self.file.close()

    def get_version(self) -> Optional[Tuple[int, int, int]]:
        if len(self.data) == 0:
            return None

        if "version" in self.data:
            return parse_version(self.data["version"])
        else:
            stderr.write("Cannot find 'version' field in the file\n")
            return None


def main(ctx, args):
    if args.command == "get":
        ver = ctx.get_version()

        if ver == None:
            stdout.write(VERSION)
        else:
            stdout.write(".".join(map(str, ver)))

    elif args.command == "set":
        ver = parse_version(args.version)

        if ver == None:
            return

        v = ".".join(map(str, ver))
        ctx.write_version(v)
        if args.push:
            ctx.push(f"set version to {v}", args.tag)

    elif args.command == "up":
        ver = ctx.get_version()

        if ver == None:
            return

        major, minor, patch = ver

        if args.component == "major":
            major += 1
            minor, patch = 0, 0
        elif args.component == "minor":
            minor += 1
            patch = 0
        elif args.component == "patch":
            patch += 1

        v = f"{major}.{minor}.{patch}"
        ctx.write_version(v)

        if args.push:
            o = ".".join(map(str, ver))
            ctx.push(f"version up from {o} to {v}", args.tag)

    elif args.command == "down":
        ver = ctx.get_version()

        if ver == None:
            return

        major, minor, patch = ver

        if args.component == "major":
            major -= 1
        elif args.component == "minor":
            minor -= 1
        elif args.component == "patch":
            patch -= 1

        v = f"{major}.{minor}.{patch}"
        if major < 0 or minor < 0 or patch < 0:
            stderr.write(f"A version component cannot be negative {v}\n")
            return

        ctx.write_version(v)
        if args.push:
            o = ".".join(map(str, ver))
            ctx.push(f"version down from {o} to {v}", args.tag)
"""


def run():
    # parse command line arguments
    args = parser.parse_args()

    if args.version:
        print(VERSION)
        exit(0)
