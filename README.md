<p align="center">
  <img src="readme/logo.png" alt="drawing" />
</p>
<h1 align="center">Verbum</h1>
<p align="center">
  <a href="https://github.com/chocolacula/verbum/actions/workflows/mypy.yml"><img src="https://github.com/chocolacula/verbum/actions/workflows/mypy.yml/badge.svg" alt="mypy"></a>
  <a href="https://github.com/chocolacula/verbum/actions/workflows/test.yml"><img src="https://github.com/chocolacula/verbum/actions/workflows/test.yml/badge.svg" alt="test"></a>
</p>

Language agnostic **VER**sion **BUM**p tool that simplifies routine version management. Its capabilities include:

- `set` version, `up` or `down` specific version component
- modify the version in the source code, make a commit, and create a tag
- analyze git history to automatically determine which component to increment
- support monorepos, you can manage a few versions in one repo
- support squash commits
- be easily customized to fit your needs!

It similar to [bumpr](https://github.com/noirbizarre/bumpr), [tbump](https://github.com/your-tools/tbump) or [bump2version](https://github.com/c4urself/bump2version?tab=readme-ov-file) but does most of work automatically.

## Installation

Make sure Python 3.9 or later, along with `pip` or `pipx`, is installed.

```sh
pip install git+https://github.com/chocolacula/verbum.git
```

## Usage

To get current version call:

```sh
verbum get
```

## Contributing

If you are not familiar with Python, I recommend create a virtual environment first, then install dev dependencies:

```sh
python3 -m venv .venv

source ./.venv/bin/activate

pip install -r requirements.txt
```
