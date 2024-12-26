<p align="center">
  <img src="https://raw.githubusercontent.com/chocolacula/verbum/refs/heads/main/readme/logo.png" alt="logo" />
</p>
<h1 align="center">Verbum</h1>
<p align="center">
  <a href="https://github.com/chocolacula/verbum/actions/workflows/mypy.yml"><img src="https://github.com/chocolacula/verbum/actions/workflows/mypy.yml/badge.svg" alt="mypy" /></a>
  <a href="https://github.com/chocolacula/verbum/actions/workflows/test.yml"><img src="https://github.com/chocolacula/verbum/actions/workflows/test.yml/badge.svg" alt="test" /></a>
  <a href="https://codecov.io/gh/chocolacula/verbum"><img src="https://codecov.io/gh/chocolacula/verbum/graph/badge.svg?token=KBSAZR4JKI" alt="codecov" /></a>
  <a href="https://docs.python.org/3/whatsnew/3.9.html"><img src="https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=fff" alt="python3.9" /></a>
  <a href="https://pypi.org/project/verbum"><img src="https://img.shields.io/pypi/v/verbum?logo=pypi&logoColor=fff" alt="pypi" /></a>
  <a href="https://pypi.org/project/verbum"><img src="https://img.shields.io/pypi/dm/verbum" alt="downloads" /></a>
</p>

Language agnostic **VER**sion **BUM**p tool that simplifies routine version management. Its capabilities include:

- `set` version, `up` or `down` specific version component
- modify the version in the source code, make a commit, and create a tag
- analyze git history to automatically determine which component to increment
- support monorepos, you can manage a few versions in one repo
- support squash commits
- be easily customized to fit your needs!

It similar to [bumpr](https://github.com/noirbizarre/bumpr), [tbump](https://github.com/your-tools/tbump) or [bump2version](https://github.com/c4urself/bump2version?tab=readme-ov-file) but it automates most of the work.

## Installation

Make sure Python 3.9 or later, along with `pip` or `pipx`, is installed.

```sh
pipx install verbum
```

## Usage

To begin, you need a configuration file. You can use `verbum` to generate a well documented default configuration file by running the following command:

```sh
cd /path/to/project

verbum init
```

It will attempt to retrieve the current version from the latest `git` tag, as well as the user's name and email. If these attempts are unsuccessful, it will use default placeholders instead. The current [version.yml](./version.yml) in the project is an ideal example of a default configuration file.

The basic commands are `get` and `set`:

```sh
verbum get

verbum set 0.1.3-rc
```

It's possible to ensure version consistency across all source files:

```sh
verbum validate --file /path/to/version.yml
```

> Most commands support the `--file` option and can be executed from a different directory.

You can increment or decrement a specific component of the semantic versioning by:

```sh
verbum up patch
verbum down minor
```

However, the most intriguing option is to analyze the output of `git log` and decide which component to increment. With the following options it updates source files, creates a commit and tag, and pushes these changes to the repository with a single command:

```sh
verbum up auto --commit --tag --push
```

Verbum follows the [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/) style but is slightly relaxed by default.
It checks both the commit message and the description. This enables the analysis of GitHub and GitLab **squash** commits, which gather all commits in the description each beginning with an `*` asterisk symbol.

Commit tags for specific version components can be easily customized in the configuration file using regular expressions.

If your project includes multiple subprojects and you want to use separate `version.yml` files, it can become challenging due to the `git log` containing commits that affect multiple subprojects simultaneously. To address this, use the `--filter` argument.

```sh
verbum up auto --filter '/src/subproject1/.*' '/src/common/.*'
```

And files that have been changed but do not match the specified regex will be excluded from the log.

## Contributing

If you are not familiar with Python, I recommend create a virtual environment first, then install dev dependencies:

```sh
python3 -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt
```
