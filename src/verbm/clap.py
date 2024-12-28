from argparse import ArgumentParser


def __add_file(p: ArgumentParser):
    p.add_argument("-f", "--file", help="specify configuration file")


def __add_common(p: ArgumentParser):
    p.add_argument("-c", "--commit", help="commit changes", action="store_true")
    p.add_argument("-t", "--tag", help="add a tag with version", action="store_true")
    p.add_argument("-p", "--push", help="push changes", action="store_true")
    __add_file(p)


def parser() -> ArgumentParser:
    p = ArgumentParser(description="version manipulating tool")

    sub = p.add_subparsers(dest="command")

    # fmt: off
    p.add_argument(
        "-v", "--version",
        help="print verbm version",
        action="store_true",
        default=False
    )


    _ = sub.add_parser(
        "init",
        description=f"create a default configuration file",
    )


    pget = sub.add_parser(
        "get",
        description=f"print current version",
    )
    __add_file(pget)


    pset = sub.add_parser(
        "set",
        description="write version to the file"
    )
    pset.add_argument(
        "new_version",
        help="semantic version in <major.minor.patch> format",
        type=str
    )
    __add_common(pset)


    pval = sub.add_parser(
        "validate",
        description="check that all files contains the same version"
    )
    __add_file(pval)


    version_components = ["major", "minor", "patch"]

    pup = sub.add_parser(
        "up",
        description="up version"
    )
    pup.add_argument(
        "component",
        help="component of semantic version",
        type=str,
        choices=version_components+["auto"],
    )
    pup.add_argument(
        "-F", "--filter",
        nargs='+',
        type=str,
        default=[],
        help="optional regex file filter for a commit",
    )
    __add_common(pup)


    pdown = sub.add_parser(
        "down",
        description="down version"
    )
    pdown.add_argument(
        "component",
        help="component of semantic version",
        type=str,
        choices=version_components,
    )
    __add_common(pdown)
    # fmt: on

    return p
