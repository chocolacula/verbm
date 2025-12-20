from os import path
import re
from typing import Tuple
from .version_control.interface import VersionControl
from .config.config import DEFAULT_FILENAMES
from .template import TEMPLATE


def __version(vc: VersionControl) -> Tuple[str, str, str]:
    tm = re.compile("v?([0-9]+)\.([0-9]+)\.([0-9]+)")

    if (t := vc.last_tag()) is not None:
        m = re.match(tm, t)
        if m:
            return (m.group(1), m.group(2), m.group(3))
        else:
            print("cannot parse the last tag, use a default")
    else:
        print("cannot get the last tag, use a default")

    return ("0", "0", "0")


def init_project(dir: str, vc: VersionControl):
    # check existing of the config file first
    for fn in DEFAULT_FILENAMES:
        if path.exists(path.join(dir, fn)):
            raise Exception(
                f"directory '{dir}' contains {fn}, the project is already initialized"
            )

    major, minor, patch = __version(vc)

    username = vc.username()
    if not username:
        print("cannot get the username, use a placeholder")
        username = "John Doe"

    email = vc.email()
    if not email:
        print("cannot get the email, use a placeholder")
        email = "john.doe@example.com"

    yaml = TEMPLATE.format(
        major=major, minor=minor, patch=patch, username=username, email=email
    )

    with open(path.join(dir, DEFAULT_FILENAMES[0]), "w") as file:
        file.write(yaml)
