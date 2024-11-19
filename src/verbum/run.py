import copy
from verbum.clap import parser
from verbum.config.config import Config
from verbum.version import Version
from verbum.source import SourceManager

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

    # we are reade to check all other commands
    v2 = copy.copy(v)
    msg = ""

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
