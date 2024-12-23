from os import path
import re
from typing import Tuple
from .version_control.interface import VersionControl
from .config.config import DEFAULT_FILENAMES


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

    yaml = f"""# main field, required
version: {major}.{minor}.{patch}

# template is needed for validation and splitting into components
# $major   integer, required
# $minor   integer, recommended
# $patch   integer, recommended
# $suffix  string,  optional
template: $major.$minor.$patch$suffix

# a list of source code files and corresponding patterns for version updates
# use `$version` as a placeholder
source:
  # - file: ./main.txt
  #   template: VERSION = "$version"


version_control:
  # default and single type, meaningless at this point
  # type: git

  commit:
    # the committer's username and email if different from the commit author from `git config`
    username: {username}
    email: {email}

    # commit message template, use `$version` and `$new_version` as placeholders, optional
    message: Version bumped from $version to $new_version

  # supports `$version` and `$new_version` placeholders the same as commit message, optional
  tag: v$new_version

  # default regex matchers for different version componets, optional
  matcher:
    major:
      - '^(\* ?)?(hot)?fix ?(\(( ?\w)+\))?!: '
      - '^(\* ?)?feat(ure)? ?(\(( ?\w)+\))?!: '
      - '^(\* ?)?refactor(ing)? ?(\(( ?\w)+\))?!: '
      - '(?i)^(\* ?)?BREAKING(?:\s*CHANGE)? ?(\(( ?\w)+\))?: '
    minor:
      - '^(\* ?)?feat(ure)? ?(\(( ?\w)+\))?: '
    patch:
      - '^(\* ?)?(hot)?fix ?(\(( ?\w)+\))?: '
      - '^(\* ?)?refactor(ing)? ?(\(( ?\w)+\))?: '
"""

    with open(path.join(dir, DEFAULT_FILENAMES[0]), "w") as file:
        file.write(yaml)
