from argparse import ArgumentParser


def parser() -> ArgumentParser:
    p = ArgumentParser(description="version manipulating utility")

    sub = p.add_subparsers(dest="command")

    # fmt: off
    p.add_argument(
        "-v", "--version",
        help="print verbum version",
        action="store_true",
        default=False
    )

    pget = sub.add_parser(
        "get",
        description=f"print current version",
    )
    pget.add_argument(
        "-f", "--file",
        help="specify configuration file"
    )


    pset = sub.add_parser(
        "set",
        description="write version to the file"
    )
    pset.add_argument(
        "version",
        help="semantic version in <major.minor.patch> format",
        type=str
    )
    pset.add_argument(
        "-t", "--tag",
        help="add a tag with version",
        action="store_true"
    )
    pset.add_argument(
        "-p", "--push",
        help="push changes",
        action="store_true"
    )
    pset.add_argument(
        "-f", "--file",
        help="specify configuration file"
    )

    version_components = ["major", "minor", "patch"]

    pup = sub.add_parser(
        "up",
        description="up version"
    )
    pup.add_argument(
        "component",
        help="component of semantic version",
        type=str,
        choices=version_components,
    )
    pup.add_argument(
        "-t", "--tag",
        help="add a tag with version",
        action="store_true"
    )
    pup.add_argument(
        "-p", "--push",
        help="push changes",
        action="store_true"
    )
    pup.add_argument(
        "-f", "--file",
        help="specify manifest file"
    )


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
    pdown.add_argument(
        "-t", "--tag",
        help="add a tag with version",
        action="store_true"
    )
    pdown.add_argument(
        "-p", "--push",
        help="push changes",
        action="store_true"
    )
    pdown.add_argument(
        "-f", "--file",
        help="specify manifest file"
    )
    # fmt: on

    return p
