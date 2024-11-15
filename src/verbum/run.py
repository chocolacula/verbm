import copy
from verbum.clap import parser
from verbum.config.config import Config
from verbum.version import Version
from verbum.source import SourceManager

VERSION = "0.0.0"

"""
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

    if args.command == "set":
        v2 = copy.copy(v)
        v2.parse(args.new_version)

        source.replace(v, v2)
        print(f"version was set to {v2}")
        exit(0)
