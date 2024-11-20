import copy
from string import Template
from verbum.clap import parser
from verbum.config.config import Config
from verbum.config.version_control import Type as VcType
from verbum.version import Version
from verbum.source import SourceManager
from verbum.version_control.git import Git
from verbum.version_control.interface import VersionControl

VERSION = "0.0.0"


def run():
    # parse command line arguments
    args = parser().parse_args()

    if args.version:
        print(VERSION)
        exit(0)

    cfg = Config.from_file(args.file)

    v = Version(format=cfg.template)
    v.parse(cfg.version)

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
    msg = ""

    vc: VersionControl
    if cfg.version_control.type == VcType.GIT:  # always true for now
        vc = Git()
    else:
        raise Exception("unexpected version control type")

    if args.command == "set":
        v2.parse(args.new_version)

        msg = f"version was set to {v2}"

    elif args.command == "up":
        if args.component == "major":
            v2.major += 1
            v2.minor, v2.patch = 0, 0
        elif args.component == "minor":
            v2.minor += 1
            v2.patch = 0
        elif args.component == "patch":
            v2.patch += 1

        msg = f"version bumped to {v2}"

    elif args.command == "down":
        if args.component == "major":
            v2.major -= 1
        elif args.component == "minor":
            v2.minor -= 1
        elif args.component == "patch":
            v2.patch -= 1

        if v2.major < 0 or v2.minor < 0 or v2.patch < 0:
            raise Exception(f"version component cannot be negative {v2}")

        msg = f"version downgraded to {v2}"

    print(msg)
    source.replace(v, v2)

    if args.commit:
        vc.add(*source.files())

        msg = Template(cfg.version_control.commit.message).substitute(
            version=str(v), new_version=str(v2)
        )
        vc.commit(
            msg,
            username=cfg.version_control.commit.username,
            email=cfg.version_control.commit.email,
        )

    if args.tag:
        tag = Template(cfg.version_control.tag).substitute(new_version=str(v2))
        vc.tag(tag)

    if args.push:
        vc.push(args.tag)
