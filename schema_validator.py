"""Checks to ensure the individual issues toml have all the required fields."""
import os
import sys
import toml

SEVERITIES = ("major", "minor", "critical")

CATEGORIES = (
    "bug-risk",
    "doc",
    "style",
    "antipattern",
    "coverage",
    "security",
    "performance",
    "typecheck",
)

GITHUB_WORKSPACE_PATH = os.environ.get("GITHUB_WORKSPACE")


def raise_issue(filepath, message, line=1, col=0):
    """
    Print the issue to stdout.

    Since we have checks on fields here, it isn't possible
    to get exact line and column.
    So, we will add issues in the last line of each file.
    """

    with open(filepath) as fp:
        line = len(fp.readlines())

    print(f"{filepath}: {line}:{col}: {message}")


def main():
    """Validate the issue toml files."""
    issues_dir = os.path.join(
        GITHUB_WORKSPACE_PATH, os.environ.get("INPUT_ISSUES-PATH", "issues/")
    )

    issue_count = 0

    for dir_path, _, filenames in os.walk(issues_dir):
        for filename in filenames:
            filepath = os.path.join(dir_path, filename)
            with open(filepath) as fp:
                try:
                    data = toml.load(fp)
                except toml.decoder.TomlDecodeError as exc:
                    # Can not decode toml file. Raise an issue.
                    # Details are in exc.
                    raise_issue(filepath, str(exc))
                    issue_count += 1
                    continue

                # Check for issue title:
                title = data.get("title")
                if not title:
                    raise_issue(filepath, f"Missing title in {filename}")
                    issue_count += 1
                else:
                    if title.endswith("."):
                        raise_issue(
                            filepath, "Issue title should not have a period `.`"
                        )
                        issue_count += 1

                # check for severity:
                severity = data.get("severity")
                if not severity:
                    raise_issue(filepath, f"Missing severity field")
                    issue_count += 1
                else:
                    if severity not in SEVERITIES:
                        raise_issue(filepath, f"severity should be one of {SEVERITIES}")
                        issue_count += 1

                # check for category
                category = data.get("category")
                if not category:
                    raise_issue(filepath, f"Missing category field")
                    issue_count += 1
                else:
                    if category not in CATEGORIES:
                        raise_issue(filepath, f"category should be one of {CATEGORIES}")
                        issue_count += 1

                # Check for description
                description = data.get("description")
                if not description:
                    raise_issue(filepath, f"Missing description field")
                    issue_count += 1
                else:
                    if not isinstance(description, str):
                        raise_issue(filepath, "Description is not a string")
                        issue_count += 1

                # if issue is recommended: make sure it is a boolean value
                recommended = data.get("recommended")
                if recommended:
                    if not isinstance(recommended, bool):
                        raise_issue(
                            filepath, "`is_recommended` should have a boolean value"
                        )
                        issue_count += 1

                # If any of autofix_available or autofix_title is present, check autofix attrs
                if "autofix_title" in data or "autofix_available" in data:
                    if not isinstance(data.get("autofix_title"), str):
                        raise_issue(filepath, "Autofix title is not a string")
                        issue_count += 1
                    if not isinstance(data.get("autofix_available"), bool):
                        raise_issue(
                            filepath, "`autofix_available` should have a boolean value"
                        )
                        issue_count += 1

    if issue_count == 0:
        sys.exit(0)
    else:
        print(f"{issue_count} issues raised.")
        sys.exit(1)


if __name__ == "__main__":
    main()
