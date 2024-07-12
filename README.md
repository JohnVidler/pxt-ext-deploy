# pxt-ext-deploy

A simple(ish) python3 script to automate some basic checks, and to increment your version numbers correctly when deploying Makecode extensions from vscode (or other external editors).

## Usage

Copy `deploy.py` into the root of your extension (the same directory as `pxt.json`) then run with `python3 deploy.py` (or `./deploy.py` if you mark it as executable).

By default this will attempt to update `pxt.json` and your git tags to match the next valid patch version (`0.0.x`), and commit it into your repository.

## Arguments

- `--major` - Increment the major version number (Resets the minor and patch versions)
- `--minor` - Increment the minor version number (Resets the patch version)
- `--patch` - Increment the patch version number. This is the default operation, so can be omitted but is included for completeness.
- `-m` or `--message` - Set a custom commit message for the changes in git.