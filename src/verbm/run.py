import copy
import re
from string import Template
from typing import List, Optional

from .clap import parser
from .config.config import Config
from .config.version_control import Matcher
from .version import Version
from .source import SourceManager
from .version_control.git import Git
from .version_control.interface import VersionControl
from .init import init_project

VERSION = "0.1.0"


def __to_component(commits: List[str], matcher: Matcher) -> Optional[str]:
    print("Commits to analyse:\n")
    for commit in commits:
        print(commit)

    for commit in commits:
        for r in matcher.major:
            if re.match(r, commit):
                return "major"

    for commit in commits:
        for r in matcher.minor:
            if re.match(r, commit):
                return "minor"

    for commit in commits:
        for r in matcher.patch:
            if re.match(r, commit):
                return "patch"

    return None


def run():
    # parse command line arguments
    args = parser().parse_args()

    vc = Git()
    if args.command == "init":
        init_project(".", vc)

    if args.version:
        print(VERSION)
        exit(0)

    cfg = Config.from_file(args.file)

    v = Version(format=cfg.template, version=cfg.version)

    if args.command == "get":
        print(v)
        exit(0)

    source = SourceManager(cfg.path, cfg.source)
    if not source.consistent(v):
        raise Exception("version is not consistent accross all files")

    if args.command == "validate":
        # already checked anyway, just print result
        print(f"version {v} is consistent accors all files")
        exit(0)

    # we are ready to check all other commands
    v2 = copy.copy(v)
    report = ""

    if args.command == "set":
        v2.parse(args.new_version)

        report = f"version was set to {v2}"

    elif args.command == "up":
        if args.component == "auto":
            filters = list(map(re.compile, args.filter))

            tag = Template(cfg.version_control.tag).substitute(new_version=str(v))

            component = __to_component(
                vc.log(tag, filters), cfg.version_control.matcher
            )
            if component == None:
                print("\nnothing to up")
                exit(0)
            else:
                print(f"\ncomponent to up: {component}")
                args.component = component

        if args.component == "major":
            v2.major += 1
            v2.minor, v2.patch = 0, 0
        elif args.component == "minor":
            v2.minor += 1
            v2.patch = 0
        elif args.component == "patch":
            v2.patch += 1

        report = f"version bumped to {v2}"

    elif args.command == "down":
        if args.component == "major":
            v2.major -= 1
        elif args.component == "minor":
            v2.minor -= 1
        elif args.component == "patch":
            v2.patch -= 1

        if v2.major < 0 or v2.minor < 0 or v2.patch < 0:
            raise Exception(f"version component cannot be negative {v2}")

        report = f"version downgraded to {v2}"

    source.replace(v, v2)
    print(report)

    # almost done, commit and push work
    if args.commit:
        vc.add(*source.files())

        report = Template(cfg.version_control.commit.message).substitute(
            version=str(v), new_version=str(v2)
        )
        vc.commit(
            report,
            username=cfg.version_control.commit.username,
            email=cfg.version_control.commit.email,
        )

    if args.tag:
        tag = Template(cfg.version_control.tag).substitute(new_version=str(v2))
        vc.tag(tag)

    if args.push:
        vc.push(args.tag)
