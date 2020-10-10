#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess  # skipcq: BAN-B404


MISSPELL_CLI_PATH = "/app/bin/misspell"

GITHUB_WORKSPACE_PATH = os.environ.get("GITHUB_WORKSPACE")


def main() -> None:
    """
    Spell check and validate issue's toml files.
    """

    issues_dir = os.getenv("INPUT_ISSUES-PATH", "/issues")
    issues_path = os.path.join(GITHUB_WORKSPACE_PATH, issues_dir)

    # Run spell checker
    command = [
        MISSPELL_CLI_PATH,
        issues_path
    ]

    # change the current working directory to the GitHub repository's context
    os.chdir(GITHUB_WORKSPACE_PATH)

    # skipcq: BAN-B603, PYL-W1510
    process = subprocess.run(
        command,
        capture_output=True,
    )


if __name__ == "__main__":
    main()
